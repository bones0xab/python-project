"""
Example script demonstrating standalone usage of the API testing framework
without pytest, for direct integration into CI/CD pipelines or custom workflows.
"""

from api_testing.core.api_client import APIClient
from api_testing.core.config import Config
from api_testing.integrations import JiraIntegration, AzureDevOpsIntegration
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_api_tests():
    """Run API tests and collect results"""
    # Load configuration
    config = Config(config_file='config.yaml')
    api_config = config.get_api_config()
    
    # Create API client (using JSONPlaceholder as example)
    base_url = api_config.get('base_url', 'https://jsonplaceholder.typicode.com')
    client = APIClient(base_url=base_url)
    
    test_results = []
    
    # Test 1: Get all posts
    logger.info("Running Test 1: Get all posts")
    try:
        response = client.get('/posts')
        if response.status_code == 200 and len(response.json()) > 0:
            test_results.append({
                'title': 'GET /posts - Fetch all posts',
                'name': 'test_get_all_posts',
                'outcome': 'Passed',
                'status': 'Pass',
                'duration_ms': int(response.elapsed.total_seconds() * 1000)
            })
            logger.info("✓ Test 1 passed")
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        test_results.append({
            'title': 'GET /posts - Fetch all posts',
            'name': 'test_get_all_posts',
            'outcome': 'Failed',
            'status': 'Fail',
            'duration_ms': 0,
            'error_message': str(e)
        })
        logger.error(f"✗ Test 1 failed: {str(e)}")
    
    # Test 2: Get single post
    logger.info("Running Test 2: Get single post")
    try:
        response = client.get('/posts/1')
        if response.status_code == 200:
            post = response.json()
            if 'id' in post and 'title' in post:
                test_results.append({
                    'title': 'GET /posts/1 - Fetch single post',
                    'name': 'test_get_single_post',
                    'outcome': 'Passed',
                    'status': 'Pass',
                    'duration_ms': int(response.elapsed.total_seconds() * 1000)
                })
                logger.info("✓ Test 2 passed")
            else:
                raise Exception("Missing required fields in response")
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        test_results.append({
            'title': 'GET /posts/1 - Fetch single post',
            'name': 'test_get_single_post',
            'outcome': 'Failed',
            'status': 'Fail',
            'duration_ms': 0,
            'error_message': str(e)
        })
        logger.error(f"✗ Test 2 failed: {str(e)}")
    
    # Test 3: Create post
    logger.info("Running Test 3: Create post")
    try:
        new_post = {
            'title': 'Test Post',
            'body': 'This is a test post',
            'userId': 1
        }
        response = client.post('/posts', json=new_post)
        if response.status_code == 201:
            test_results.append({
                'title': 'POST /posts - Create new post',
                'name': 'test_create_post',
                'outcome': 'Passed',
                'status': 'Pass',
                'duration_ms': int(response.elapsed.total_seconds() * 1000)
            })
            logger.info("✓ Test 3 passed")
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except Exception as e:
        test_results.append({
            'title': 'POST /posts - Create new post',
            'name': 'test_create_post',
            'outcome': 'Failed',
            'status': 'Fail',
            'duration_ms': 0,
            'error_message': str(e)
        })
        logger.error(f"✗ Test 3 failed: {str(e)}")
    
    return test_results


def report_to_jira(test_results):
    """Report test results to Jira"""
    try:
        config = Config(config_file='config.yaml')
        jira_config = config.get_jira_config()
        
        if not all(jira_config.values()):
            logger.warning("Jira not configured, skipping Jira reporting")
            return
        
        logger.info("Reporting to Jira...")
        jira = JiraIntegration(
            server=jira_config['server'],
            username=jira_config['username'],
            api_token=jira_config['api_token'],
            project_key=jira_config['project_key']
        )
        
        issue_key = jira.create_test_execution_issue(
            test_cases=test_results,
            execution_summary=f"Automated API Test Execution - {len(test_results)} tests"
        )
        
        if issue_key:
            logger.info(f"✓ Test results reported to Jira: {issue_key}")
        else:
            logger.error("✗ Failed to report to Jira")
    
    except Exception as e:
        logger.error(f"Error reporting to Jira: {str(e)}")


def report_to_azure_devops(test_results):
    """Report test results to Azure DevOps"""
    try:
        config = Config(config_file='config.yaml')
        azure_config = config.get_azure_devops_config()
        
        if not (azure_config.get('organization_url') and 
                azure_config.get('project') and 
                azure_config.get('personal_access_token')):
            logger.warning("Azure DevOps not configured, skipping Azure DevOps reporting")
            return
        
        logger.info("Reporting to Azure DevOps...")
        azure = AzureDevOpsIntegration(
            organization_url=azure_config['organization_url'],
            project=azure_config['project'],
            personal_access_token=azure_config['personal_access_token']
        )
        
        plan_id = azure_config.get('test_plan_id')
        if plan_id:
            plan_id = int(plan_id)
        
        run_id = azure.report_test_execution(
            test_name="Automated API Test Execution",
            test_results=test_results,
            plan_id=plan_id
        )
        
        if run_id:
            logger.info(f"✓ Test results reported to Azure DevOps: Run ID {run_id}")
        else:
            logger.error("✗ Failed to report to Azure DevOps")
    
    except Exception as e:
        logger.error(f"Error reporting to Azure DevOps: {str(e)}")


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("Starting API Test Execution")
    logger.info("=" * 60)
    
    # Run tests
    test_results = run_api_tests()
    
    # Print summary
    logger.info("=" * 60)
    logger.info("Test Execution Summary")
    logger.info("=" * 60)
    passed = sum(1 for r in test_results if r['outcome'] == 'Passed')
    failed = sum(1 for r in test_results if r['outcome'] == 'Failed')
    logger.info(f"Total Tests: {len(test_results)}")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    logger.info("=" * 60)
    
    # Report to integrations
    report_to_jira(test_results)
    report_to_azure_devops(test_results)
    
    logger.info("=" * 60)
    logger.info("Test execution completed")
    logger.info("=" * 60)
    
    # Exit with appropriate code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
