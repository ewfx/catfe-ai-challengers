from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from typing import Dict, List

class JiraLLMProcessor:
    """Process Jira data using LLM capabilities."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(api_key=api_key, model_name=model_name)
    
    def generate_test_cases_from_issue(self, issue_data: Dict) -> str:
        """Generate test cases from a Jira issue using LLM."""
        prompt_template = PromptTemplate(
            input_variables=["issue_summary", "issue_description"],
            template="""
            Generate BDD-style test cases for the following Jira issue:
            
            Summary: {issue_summary}
            Description: {issue_description}
            
            The test cases should follow the Gherkin syntax with "Given", "When", and "Then" steps.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        return chain.run({
            "issue_summary": issue_data["fields"]["summary"],
            "issue_description": issue_data["fields"]["description"]
        })
    
    def summarize_test_results(self, test_results: List[Dict]) -> str:
        """Generate a summary of test results for Jira comments."""
        prompt_template = PromptTemplate(
            input_variables=["test_results"],
            template="""
            Summarize the following test results in a concise format suitable for a Jira comment:
            
            {test_results}
            
            Include overall pass/fail status, key failures, and recommendations.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        return chain.run({
            "test_results": str(test_results)
        })
