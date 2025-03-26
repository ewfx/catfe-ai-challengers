from git import Repo, InvalidGitRepositoryError
import os
import shutil
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

def is_valid_content(content):
    """
    Validate content to exclude problematic text.
    
    Args:
        content (str): The content to validate.
        
    Returns:
        bool: True if content is valid, False otherwise.
    """
    # Add validation logic here
    return True

def store_git_files_in_vectordb(repo_url, repo_path, openai_api_key):
    """
    Clone a Git repository, read source code files, and store their details in a FAISS vector database.

    Args:
        repo_url (str): URL of the Git repository.
        repo_path (str): Local path to clone the repository.
        openai_api_key (str): OpenAI API key for generating embeddings.

    Returns:
        FAISS: A FAISS vector store containing the embeddings of the source code files.
    """
    # Set OpenAI API key
    print(f"OPENAI_API_KEY: {openai_api_key}")
    os.environ["OPENAI_API_KEY"] = "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"
    # Check if repo_path is valid
    if not repo_path:
        raise ValueError("Repository path cannot be empty")
    
    # Create parent directory if it doesn't exist
    parent_dir = os.path.dirname(repo_path)
    if parent_dir:  # Only try to create if parent_dir is not empty
        os.makedirs(parent_dir, exist_ok=True)

    # Clone or pull the latest from the repository
    if os.path.exists(repo_path):
        try:
            # Try to use it as a Git repository
            repo = Repo(repo_path)
            # If successful, pull the latest changes
            repo.git.pull()
        except InvalidGitRepositoryError:
            # If it's not a valid Git repository, remove it and clone
            print(f"Directory {repo_path} exists but is not a valid Git repository. Removing and cloning...")
            shutil.rmtree(repo_path)
            repo = Repo.clone_from(repo_url, repo_path)
    else:
        # Directory doesn't exist, clone the repository
        os.makedirs(os.path.dirname(repo_path), exist_ok=True)
        repo = Repo.clone_from(repo_url, repo_path)

    # Read all source code files
    source_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".js", ".java", ".cs")):  # Adjust based on your codebase
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Validate content to exclude problematic text
                        if is_valid_content(content):
                            source_files.append({"file_path": file_path, "content": content})
                        else:
                            print(f"Excluded file due to invalid content: {file_path}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    # Create embeddings and store in FAISS
    if not source_files:
        print("No source files found in the repository.")
        return None
        
    texts = [f["content"] for f in source_files]
    metadatas = [{"file_path": f["file_path"]} for f in source_files]
    
    embeddings = OpenAIEmbeddings(openai_api_key="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")
    vector_store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    
    return vector_store
