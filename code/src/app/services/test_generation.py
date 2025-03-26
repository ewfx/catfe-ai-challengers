from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
import json
import os
import subprocess
from git import Repo, InvalidGitRepositoryError

# !pip install chromadb
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.language.language_parser import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.embeddings import OpenAIEmbeddings



def generate_test_cases_and_store_in_faiss(openai_api_key, vector_store=None):
    """
    Generate test cases and store them in a FAISS vector database.
    
    Args:
        openai_api_key (str): OpenAI API key.
        vector_store (FAISS, optional): Existing vector store to use.
        
    Returns:
        FAISS: A FAISS vector store containing the test cases.
    """
    # If a vector store is provided, use it
    if vector_store:
        return vector_store
    
    # Otherwise, create a new one (this is a fallback and should be improved)
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    
    # Set OpenAI API key
    import os
    os.environ["OPENAI_API_KEY"] = openai_api_key
    
    # Create a simple vector store with a placeholder
    embeddings = OpenAIEmbeddings()
    texts = ["API endpoint for customer creation accepts POST requests with customer details and returns 201 Created on success."]
    vector_store = FAISS.from_texts(texts=texts, embedding=embeddings)
    
    return vector_store


def generate_bdd_test_cases_json(vector_store, query, model_name="gpt-4"):
    """
    Generate BDD-style test cases based on the retrieved response from a FAISS vector store.

    Args:
        vector_store (FAISS): The FAISS vector store containing API data.
        query (str): The query to search for relevant documents in the vector store.
        model_name (str): The name of the OpenAI model to use for generating test cases.

    Returns:
        str: The generated BDD test cases in JSON format.
    """
    # Query the vector store for relevant documents
    retriever = vector_store.as_retriever()
    retrieved_response = retriever.get_relevant_documents(query)

    if not retrieved_response:
        print("No relevant documents found for the query.")
        return None

    # Extract the response body from the retrieved documents
    response_body = retrieved_response[0].page_content

    # Define a prompt template for generating BDD test cases
    bdd_test_case_template = PromptTemplate(
        input_variables=["response_body"],
        template="""
        Generate BDD-style test cases for the following API:
        Expected Response:
        {response_body}

        The test cases should follow the Gherkin syntax with "Given", "When", and "Then" steps.
        Format the output as a JSON array of test cases.
        """
    )

    # Initialize the OpenAI model
    llm = ChatOpenAI(model_name=model_name)

    # Create an LLMChain for generating BDD test cases
    bdd_test_case_chain = LLMChain(
        llm=llm,
        prompt=bdd_test_case_template
    )

    # Generate BDD test cases
    bdd_test_cases = bdd_test_case_chain.run({"response_body": response_body})

    #Generate test case Solution starts
    test_case_name = "GenericTestCase"

    # Define the output directory for the SpecFlow project
    output_dir = "specflow_tests"
    os.makedirs(output_dir, exist_ok=True)

    # Save the feature file
    feature_file_path = os.path.join(output_dir, f"{test_case_name}.feature")
    with open(feature_file_path, "w") as file:
        file.write(bdd_test_cases)

    print(f"SpecFlow test cases saved to: {feature_file_path}")

    # Create a SpecFlow C# Project file (.csproj)
    csproj_content = f"""<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    </PropertyGroup>

    <ItemGroup>
    <PackageReference Include="SpecFlow" Version="3.9.74" />
    <PackageReference Include="SpecFlow.NUnit" Version="3.9.74" />
    <PackageReference Include="NUnit" Version="3.13.1" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.0.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.1.0" />
    </ItemGroup>

    <ItemGroup>
    <None Include="Features\{test_case_name}.feature" />
    </ItemGroup>

    </Project>"""

    # Save the .csproj file to the SpecFlow test folder
    csproj_file_path = os.path.join(output_dir, "SpecFlowProject.csproj")
    with open(csproj_file_path, "w") as file:
        file.write(csproj_content)

    #Generate Test Case Solution ends

    # Try to parse as JSON, if not already in JSON format
    try:
        bdd_test_cases_json = json.loads(bdd_test_cases)
    except json.JSONDecodeError:
        # If not valid JSON, return as string
        return bdd_test_cases

    return bdd_test_cases_json



def run_specflow_tests(specflow_project_dir):
    """
    Run the SpecFlow tests in the specified project directory and capture the output.

    Args:
        specflow_project_dir (str): Path to the SpecFlow project directory.

    Returns:
        str: The output of the test run if successful, or the error message if it fails.
    """
    # Ensure the .csproj file exists
    csproj_file = os.path.join(specflow_project_dir, "SpecFlowProject.csproj")
    if not os.path.exists(csproj_file):
        raise FileNotFoundError(f"SpecFlow project file not found: {csproj_file}")

    # Run the SpecFlow tests using `dotnet test`
    try:
        print(f"Running SpecFlow tests in: {specflow_project_dir}")
        result = subprocess.run(
            ["dotnet", "test", csproj_file],
            capture_output=True,
            text=True,
            check=True
        )
        print("SpecFlow tests executed successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error occurred while running SpecFlow tests.")
        return e.stderr




def generate_bdd_test_cases(repo_url, query, persist_directory, chunk_size=2000, chunk_overlap=200, k=5):
    #"""
    #Generates BDD test cases from a given GitHub repository and query.

    #Args:
    #    repo_url (str): URL of the GitHub repository to clone.
    #    query (str): Query to retrieve relevant information for BDD test case generation.
    #    persist_directory (str): Directory to persist the Chroma vector database.
    #    chunk_size (int): Size of the text chunks for splitting documents.
    #    chunk_overlap (int): Overlap size for text chunks.
    #    k (int): Number of relevant documents to retrieve.

    #Returns:
    #    str: Generated BDD test cases.
    #"""
    import os
    openai_api_key = "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"
    os.environ["OPENAI_API_KEY"] = openai_api_key

    # Ensure chunk_size and chunk_overlap are integers
    chunk_size = int(chunk_size)
    chunk_overlap = int(chunk_overlap)

    # Clone the GitHub repository
    repo_path = "temp_repo"
    try:
        if not os.path.exists(repo_path):
            Repo.clone_from(repo_url, to_path=repo_path)
    except Exception as e:
        raise RuntimeError(f"Failed to clone repository: {e}")

    # Load and process the repository files
    try:
        loader = GenericLoader.from_filesystem(
            repo_path,
            glob="**/*",
            suffixes=[".cs"],
            parser=LanguageParser(language=Language.CSHARP, parser_threshold=500)
        )
        documents = loader.load()
        if not documents:
            raise ValueError("No documents found in the repository.")
    except Exception as e:
        raise RuntimeError(f"Failed to load documents: {e}")

    # Split documents into chunks
    try:
        documents_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.CSHARP,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        texts = documents_splitter.split_documents(documents)
    except Exception as e:
        raise RuntimeError(f"Failed to split documents: {e}")

    # Initialize OpenAI embeddings and Chroma vector database
    try:
        os.makedirs(persist_directory, exist_ok=True)
        embeddings = OpenAIEmbeddings(disallowed_special=())
        print(persist_directory)
        vectordb = Chroma.from_documents(texts, embedding=embeddings, persist_directory=persist_directory)
        print("Vector database initialized successfully.")
        vectordb.persist()
    except Exception as e:
        raise RuntimeError(f"Failed to initialize vector database: {e}")

    # Query the vector database
    try:
        retrieved_docs = vectordb.similarity_search(query, k=k)
        if not retrieved_docs:
            raise ValueError("No relevant documents found for the query.")
        test_case_input = "\n".join([doc.page_content for doc in retrieved_docs])
    except Exception as e:
        raise RuntimeError(f"Failed to query vector database: {e}")

    # Define the BDD test case prompt template
    try:
        bdd_test_case_template = PromptTemplate(
            input_variables=["test_case_input"],
            template=(
                " Generate SpecFlow BDD all types positive and negative cases and step definitions and binding with the following parameters:\n"
                "{test_case_input}"
                #"For each test case, include:\n"
                #"- Input Request\n"
                #"- Expected Output Response\n"
                #"- Scenario Description\n"
                #"- Given, When, Then format\n"
            )
        )
    except Exception as e:
        raise RuntimeError(f"Failed to define BDD test case template: {e}")

    # Create an LLMChain for generating BDD test cases
    try:
        llm = ChatOpenAI(model_name="gpt-4")
        bdd_test_case_chain = LLMChain(llm=llm, prompt=bdd_test_case_template)
        bdd_test_cases = bdd_test_case_chain.run(test_case_input)
    except Exception as e:
        raise RuntimeError(f"Failed to generate BDD test cases: {e}")

      # Generate BDD test cases
      #bdd_test_cases = bdd_test_case_chain.run({"response_body": response_body})

    #Generate test case Solution starts
    test_case_name = "GenericTestCase"

    # Define the output directory for the SpecFlow project
    output_dir = "specflow_tests"
    os.makedirs(output_dir, exist_ok=True)

    # Save the feature file
    feature_file_path = os.path.join(output_dir, f"{test_case_name}.feature")
    with open(feature_file_path, "w") as file:
        file.write(bdd_test_cases)

    print(f"SpecFlow test cases saved to: {feature_file_path}")

    # Create a SpecFlow C# Project file (.csproj)
    csproj_content = f"""<Project Sdk="Microsoft.NET.Sdk">

    <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <LangVersion>latest</LangVersion>
    </PropertyGroup>

    <ItemGroup>
    <PackageReference Include="SpecFlow" Version="3.9.74" />
    <PackageReference Include="SpecFlow.NUnit" Version="3.9.74" />
    <PackageReference Include="NUnit" Version="3.13.1" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.0.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.1.0" />
    </ItemGroup>
    <ItemGroup>
    <None Include="Features\{test_case_name}.feature" />
    </ItemGroup>
    </Project>"""

    # Save the .csproj file to the SpecFlow test folder
    csproj_file_path = os.path.join(output_dir, "SpecFlowProject.csproj")
    with open(csproj_file_path, "w") as file:
        file.write(csproj_content)
    #Generate Test Case Solution ends   
    return bdd_test_cases