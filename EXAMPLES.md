# Examples

This directory contains example usage of the REST API Testing Framework.

## Basic Usage Example

See `run_tests.py` in the root directory for a complete standalone example.

## Custom Test Example

```python
"""
Custom API test example
"""
import pytest
from api_testing.core.api_client import APIClient


@pytest.fixture
def my_api_client():
    """Create a client for your API"""
    client = APIClient(base_url="https://api.myservice.com")
    # Set authentication
    client.set_auth("bearer", token="your-token-here")
    return client


@pytest.mark.api_test
class TestMyAPI:
    """Tests for My API"""
    
    def test_health_check(self, my_api_client):
        """Test API health endpoint"""
        response = my_api_client.get('/health')
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
    
    def test_create_resource(self, my_api_client):
        """Test resource creation"""
        payload = {
            'name': 'Test Resource',
            'description': 'A test resource'
        }
        response = my_api_client.post('/resources', json=payload)
        
        assert response.status_code == 201
        assert 'id' in response.json()
        
    def test_update_resource(self, my_api_client):
        """Test resource update"""
        payload = {
            'name': 'Updated Resource'
        }
        response = my_api_client.put('/resources/123', json=payload)
        
        assert response.status_code == 200
        assert response.json()['name'] == 'Updated Resource'
```

## Direct Integration Example

```python
"""
Using integrations directly without pytest
"""
from api_testing.integrations import JiraIntegration, AzureDevOpsIntegration

# Jira Integration
jira = JiraIntegration(
    server="https://your-instance.atlassian.net",
    username="your-email@example.com",
    api_token="your-api-token",
    project_key="TEST"
)

# Create a test issue
issue_key = jira.create_test_issue(
    summary="API Test: User Registration",
    description="Testing the user registration endpoint"
)

# Update with results
jira.update_test_result(
    issue_key=issue_key,
    status="Pass",
    comment="All assertions passed successfully"
)

# Azure DevOps Integration
azure = AzureDevOpsIntegration(
    organization_url="https://dev.azure.com/your-org",
    project="YourProject",
    personal_access_token="your-pat"
)

# Report test results
test_results = [
    {
        'title': 'Test User Login',
        'outcome': 'Passed',
        'duration_ms': 250
    },
    {
        'title': 'Test User Logout',
        'outcome': 'Passed',
        'duration_ms': 150
    }
]

run_id = azure.report_test_execution(
    test_name="User Authentication Tests",
    test_results=test_results,
    plan_id=12345  # Your test plan ID
)
```

## CI/CD Integration Example

### GitHub Actions

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run API tests
        env:
          JIRA_SERVER: ${{ secrets.JIRA_SERVER }}
          JIRA_USERNAME: ${{ secrets.JIRA_USERNAME }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_PROJECT_KEY: ${{ secrets.JIRA_PROJECT_KEY }}
          AZURE_DEVOPS_ORG_URL: ${{ secrets.AZURE_DEVOPS_ORG_URL }}
          AZURE_DEVOPS_PROJECT: ${{ secrets.AZURE_DEVOPS_PROJECT }}
          AZURE_DEVOPS_PAT: ${{ secrets.AZURE_DEVOPS_PAT }}
          API_BASE_URL: https://api.example.com
        run: |
          pytest -v
```

### Azure Pipelines

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.9'
    
  - script: |
      pip install -r requirements.txt
    displayName: 'Install dependencies'
    
  - script: |
      pytest -v
    displayName: 'Run API tests'
    env:
      JIRA_SERVER: $(JIRA_SERVER)
      JIRA_USERNAME: $(JIRA_USERNAME)
      JIRA_API_TOKEN: $(JIRA_API_TOKEN)
      JIRA_PROJECT_KEY: $(JIRA_PROJECT_KEY)
      AZURE_DEVOPS_ORG_URL: $(AZURE_DEVOPS_ORG_URL)
      AZURE_DEVOPS_PROJECT: $(AZURE_DEVOPS_PROJECT)
      AZURE_DEVOPS_PAT: $(AZURE_DEVOPS_PAT)
      API_BASE_URL: https://api.example.com
```
