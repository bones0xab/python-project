"""Pytest plugin for Jira and Azure DevOps integration"""

import pytest
import logging
from typing import Dict, List
from api_testing.core.config import Config
from api_testing.integrations import JiraIntegration, AzureDevOpsIntegration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestResultCollector:
    """Collects test results for reporting to Jira and Azure DevOps"""
    
    def __init__(self):
        self.test_results = []
    
    def add_result(self, test_name: str, outcome: str, duration: float, 
                  error_message: str = None):
        """Add a test result"""
        self.test_results.append({
            'title': test_name,
            'name': test_name,
            'outcome': outcome,
            'status': outcome,
            'duration_ms': int(duration * 1000),
            'error_message': error_message
        })
    
    def get_results(self) -> List[Dict]:
        """Get all collected results"""
        return self.test_results


# Global test result collector
test_collector = TestResultCollector()


def pytest_configure(config):
    """Pytest configuration hook"""
    config.addinivalue_line(
        "markers", "api_test: mark test as an API test"
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        test_name = item.nodeid
        outcome_status = "Passed" if report.passed else "Failed"
        duration = report.duration
        error_message = str(report.longrepr) if report.failed else None
        
        test_collector.add_result(test_name, outcome_status, duration, error_message)


def pytest_sessionfinish(session, exitstatus):
    """Hook called after all tests are finished"""
    if not test_collector.test_results:
        return
    
    try:
        # Load configuration
        config = Config(config_file='config.yaml')
        
        # Report to Jira if configured
        jira_config = config.get_jira_config()
        if all(jira_config.values()):
            try:
                jira = JiraIntegration(
                    server=jira_config['server'],
                    username=jira_config['username'],
                    api_token=jira_config['api_token'],
                    project_key=jira_config['project_key']
                )
                
                jira.create_test_execution_issue(
                    test_cases=test_collector.test_results,
                    execution_summary=f"API Test Execution - {len(test_collector.test_results)} tests"
                )
                logger.info("Test results reported to Jira")
            except Exception as e:
                logger.warning(f"Could not report to Jira: {str(e)}")
        
        # Report to Azure DevOps if configured
        azure_config = config.get_azure_devops_config()
        if azure_config.get('organization_url') and azure_config.get('project') and azure_config.get('personal_access_token'):
            try:
                azure = AzureDevOpsIntegration(
                    organization_url=azure_config['organization_url'],
                    project=azure_config['project'],
                    personal_access_token=azure_config['personal_access_token']
                )
                
                plan_id = azure_config.get('test_plan_id')
                if plan_id:
                    plan_id = int(plan_id)
                
                azure.report_test_execution(
                    test_name=f"API Test Run",
                    test_results=test_collector.test_results,
                    plan_id=plan_id
                )
                logger.info("Test results reported to Azure DevOps")
            except Exception as e:
                logger.warning(f"Could not report to Azure DevOps: {str(e)}")
    
    except Exception as e:
        logger.warning(f"Could not report test results: {str(e)}")
