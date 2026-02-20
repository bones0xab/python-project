"""Azure DevOps integration for reporting test results"""

import logging
from typing import Dict, Any, Optional, List
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.test import TestClient
from azure.devops.v7_1.test.models import TestCaseResult, TestRun, RunCreateModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureDevOpsIntegration:
    """Integration with Azure DevOps for test result reporting"""
    
    def __init__(self, organization_url: str, project: str, personal_access_token: str):
        """
        Initialize Azure DevOps integration
        
        Args:
            organization_url: Azure DevOps organization URL
            project: Project name
            personal_access_token: Personal access token
        """
        self.organization_url = organization_url
        self.project = project
        
        try:
            # Create a connection to the Azure DevOps organization
            credentials = BasicAuthentication('', personal_access_token)
            self.connection = Connection(base_url=organization_url, creds=credentials)
            
            # Get the test client
            self.test_client = self.connection.clients.get_test_client()
            
            logger.info(f"Connected to Azure DevOps: {organization_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Azure DevOps: {str(e)}")
            raise
    
    def create_test_run(self, name: str, plan_id: Optional[int] = None) -> Optional[int]:
        """
        Create a test run in Azure DevOps
        
        Args:
            name: Test run name
            plan_id: Test plan ID (optional)
            
        Returns:
            Test run ID if successful, None otherwise
        """
        try:
            run_create_model = RunCreateModel(
                name=name,
                plan_id=plan_id,
                automated=True
            )
            
            test_run = self.test_client.create_test_run(
                run_create_model,
                project=self.project
            )
            
            logger.info(f"Created test run: {test_run.id} - {name}")
            return test_run.id
        except Exception as e:
            logger.error(f"Failed to create test run: {str(e)}")
            return None
    
    def update_test_results(self, run_id: int, test_results: List[Dict[str, Any]]) -> bool:
        """
        Update test results for a test run
        
        Args:
            run_id: Test run ID
            test_results: List of test results
            
        Returns:
            True if successful, False otherwise
        """
        try:
            results = []
            
            for result in test_results:
                test_case_result = TestCaseResult(
                    test_case_title=result.get('title', 'Unnamed Test'),
                    outcome=result.get('outcome', 'Failed'),  # Passed, Failed, NotExecuted
                    state='Completed',
                    automated_test_name=result.get('test_name'),
                    error_message=result.get('error_message'),
                    duration_in_ms=result.get('duration_ms', 0)
                )
                results.append(test_case_result)
            
            self.test_client.add_test_results_to_test_run(
                results,
                project=self.project,
                run_id=run_id
            )
            
            logger.info(f"Updated {len(results)} test results for run {run_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update test results: {str(e)}")
            return False
    
    def complete_test_run(self, run_id: int) -> bool:
        """
        Complete a test run
        
        Args:
            run_id: Test run ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            test_run = TestRun(
                id=run_id,
                state='Completed'
            )
            
            self.test_client.update_test_run(
                test_run,
                project=self.project,
                run_id=run_id
            )
            
            logger.info(f"Completed test run: {run_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to complete test run: {str(e)}")
            return False
    
    def report_test_execution(self, test_name: str, test_results: List[Dict[str, Any]], 
                             plan_id: Optional[int] = None) -> Optional[int]:
        """
        Report a complete test execution to Azure DevOps
        
        Args:
            test_name: Name of the test execution
            test_results: List of test results
            plan_id: Test plan ID (optional)
            
        Returns:
            Test run ID if successful, None otherwise
        """
        # Create test run
        run_id = self.create_test_run(test_name, plan_id)
        
        if run_id is None:
            return None
        
        # Update test results
        if not self.update_test_results(run_id, test_results):
            return None
        
        # Complete test run
        if not self.complete_test_run(run_id):
            return None
        
        return run_id
