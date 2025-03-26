# Libraries: fastapi, pydantic, langchain, dotenv
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

# Load Helper modules from new structure
from app.services.git_service import store_git_files_in_vectordb
from app.services.test_generation import generate_test_cases_and_store_in_faiss
from app.services.test_generation import generate_bdd_test_cases_json
from app.services.test_generation import run_specflow_tests
from app.services.test_generation import generate_bdd_test_cases
load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
app = FastAPI()
vector_store = None
openai_api_key = "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"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define Input Schema
class TextRequest(BaseModel):
    text: str

# Endpoint: process_repo
@app.post("/process_repoandgenerate_testcases")
def process_repo(request: TextRequest):
    # Example logic to process the input text
    repo_url ="https://github.com/ram541619/CustomerOnboardFlow.git"# request.text 
    #"https://github.com/ram541619/CustomerOnboardFlow.git"
    repo_path = "repo"
    # Call the function
    vector_store = store_git_files_in_vectordb(repo_url, repo_path, openai_api_key)
    # Example usage
    vector_store = generate_test_cases_and_store_in_faiss(openai_api_key)
    query = "What is the response for a valid customer creation request?"
    bdd_test_cases = generate_bdd_test_cases_json(vector_store, query)
    return {"process_repo": bdd_test_cases}


@app.post("/executetestcaseandgenerate_testresult")
def generate_testresult(request: TextRequest):
    # Example logic to process the input text
    # Define the SpecFlow project directory
    specflow_project_dir = "specflow_tests"
    repo_output=""
    # Run the SpecFlow tests and capture the output
    try:
        test_output = run_specflow_tests(specflow_project_dir)
        repo_output= test_output
        print("SpecFlow Test Output:")
        print(test_output)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        repo_output = f"Processed text: {test_output}"
    return {"generate_testresult": repo_output}


# Endpoint: process_repo
@app.post("/process_repoandgenerate_testcasesv1")
def process_repoandgenerate_testcases(request: TextRequest):
    repo_url = "https://github.com/ram541619/CustomerOnboardFlow.git"
    query = "generate BDD test cases for the Customer Onboard Flow using Specflow. code should be in Gherkin format. add input data for the test cases as well. add the test cases for the following scenarios: 1. Customer Onboard Flow with valid data 2. Customer Onboard Flow with invalid data 3. Customer Onboard Flow with duplicate data 4. Customer Onboard Flow with missing data 5. Customer Onboard Flow with special characters in the data"
    persist_directory = "./VectorDB"
    print(f"OPENAI_API_KEY: {openai_api_key}")
    bdd_test_cases = generate_bdd_test_cases(repo_url, query, persist_directory)
    return {"process_repo": bdd_test_cases}

# Run using: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
