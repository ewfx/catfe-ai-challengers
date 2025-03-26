from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from app.core.config import settings
from app.services.git_service import store_git_files_in_vectordb
from app.services.test_generation import (
    generate_test_cases_and_store_in_faiss, 
    generate_bdd_test_cases_json,
    generate_bdd_test_cases_from_repo
)
from integrations.jira.client import JiraClient
from integrations.jira.llm_processor import JiraLLMProcessor

router = APIRouter()

class TextRequest(BaseModel):
    text: str

class RepoRequest(BaseModel):
    repo_url: str
    query: str = "Retrieve all API details including methods, input parameters, and expected responses"
    file_extensions: Optional[List[str]] = [".cs", ".py", ".js"]

@router.post("/process_repoandgenerate_testcases")
def process_repo(request: TextRequest):
    """Process a Git repository and generate test cases."""
    repo_url = request.text
    repo_path = settings.REPO_PATH
    
    print(f"Processing repository: {repo_url}")
    print(f"Repository path: {repo_path}")
    print(f"OPENAPIKEY: {settings.OPENAI_API_KEY}")
    # Store Git files in vector database
    vector_store = store_git_files_in_vectordb(repo_url, repo_path, settings.OPENAI_API_KEY)
    
    if vector_store is None:
        return {"error": "Failed to create vector store from repository. No source files found."}
    
    # Generate test cases and store in FAISS
    vector_store = generate_test_cases_and_store_in_faiss(settings.OPENAI_API_KEY)
    
    if vector_store is None:
        return {"error": "Failed to generate test cases."}
    
    # Generate BDD test cases
    query = "What is the response for a valid customer creation request?"
    bdd_test_cases = generate_bdd_test_cases_json(vector_store, query)
    
    return {"process_repo": bdd_test_cases}

@router.post("/generate_bdd_test_cases")
def generate_bdd_test_cases(request: RepoRequest):
    """Generate BDD test cases from a Git repository."""
    try:
        bdd_test_cases = generate_bdd_test_cases_from_repo(
            repo_url=request.repo_url,
            query=request.query,
            openai_api_key=settings.OPENAI_API_KEY,
            file_extensions=request.file_extensions
        )
        return {"bdd_test_cases": bdd_test_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating BDD test cases: {str(e)}")

@router.post("/executetestcaseandgenerate_testresult")
def generate_testresult(request: TextRequest):
    """Execute test cases and generate test results."""
    repo_output = f"Processed text: {request.text}"
    return {"generate_testresult": repo_output}

# Jira integration endpoints
@router.post("/jira/create_test_cases")
def create_jira_test_cases(request: TextRequest):
    """Create test cases in Jira based on requirements."""
    try:
        # Initialize Jira client
        jira_client = JiraClient(
            base_url=settings.JIRA_URL,
            username=settings.JIRA_USERNAME,
            api_token=settings.JIRA_API_TOKEN
        )
        
        # Initialize LLM processor
        llm_processor = JiraLLMProcessor(api_key=settings.OPENAI_API_KEY)
        
        # Get issue data
        issue_key = request.text
        issue_data = jira_client.get_issue(issue_key)
        
        # Generate test cases
        test_cases = llm_processor.generate_test_cases_from_issue(issue_data)
        
        return {"test_cases": test_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating Jira test cases: {str(e)}")
