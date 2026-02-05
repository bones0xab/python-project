# REST API Testing Framework

A comprehensive Python framework for testing REST APIs with built-in integration for Jira and Azure DevOps. This framework allows you to write API tests and automatically report results to your project management and DevOps platforms.

## Features

- **REST API Testing**: Simple and powerful API client for testing REST endpoints
- **Jira Integration**: Automatically create and update test issues in Jira
- **Azure DevOps Integration**: Report test results to Azure DevOps Test Plans
- **Pytest Integration**: Built on pytest for familiar testing experience
- **Flexible Configuration**: Support for YAML config files and environment variables
- **Comprehensive Examples**: Includes sample tests to get you started

## Installation

1. Clone this repository:
```bash
git clone https://github.com/bones0xab/python-project.git
cd python-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode (optional):
```bash
pip install -e .
```

## Configuration

### Option 1: Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Jira Configuration
JIRA_SERVER=https://your-jira-instance.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=TEST

# Azure DevOps Configuration
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/your-organization
AZURE_DEVOPS_PROJECT=your-project-name
AZURE_DEVOPS_PAT=your-pat-token
AZURE_DEVOPS_TEST_PLAN_ID=12345

# API Testing Configuration
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
API_VERIFY_SSL=true
```

### Option 2: YAML Configuration

Copy `config.yaml.example` to `config.yaml` and update with your values:

```bash
cp config.yaml.example config.yaml
```

**Note**: Environment variables take precedence over YAML configuration.

## Usage

### Running Tests

Run all API tests:
```bash
pytest
```

Run specific test file:
```bash
pytest api_testing/tests/test_api_examples.py
```

Run tests with detailed output:
```bash
pytest -v
```

Run tests and generate HTML report:
```bash
pytest --html=report.html
```

### Writing Your Own Tests

Create a new test file in `api_testing/tests/`:

```python
import pytest
from api_testing.core.api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient(base_url="https://api.example.com")

@pytest.mark.api_test
def test_my_api_endpoint(api_client):
    """Test your API endpoint"""
    response = api_client.get('/endpoint')
    
    assert response.status_code == 200
    assert response.json()['status'] == 'success'
```

### Using the API Client Programmatically

```python
from api_testing.core.api_client import APIClient

# Create client
client = APIClient(base_url="https://api.example.com")

# Set authentication
client.set_auth("bearer", token="your-token")

# Make requests
response = client.get("/users")
print(response.json())

# POST request
response = client.post("/users", json={"name": "John Doe"})
print(response.status_code)
```

### Reporting to Jira

When tests complete, results are automatically reported to Jira if configured. You can also use Jira integration directly:

```python
from api_testing.integrations import JiraIntegration
from api_testing.core.config import Config

config = Config()
jira_config = config.get_jira_config()

jira = JiraIntegration(
    server=jira_config['server'],
    username=jira_config['username'],
    api_token=jira_config['api_token'],
    project_key=jira_config['project_key']
)

# Create test issue
issue_key = jira.create_test_issue(
    summary="API Test for User Endpoint",
    description="Testing user creation API"
)

# Update test result
jira.update_test_result(issue_key, status="Pass", comment="All tests passed")
```

### Reporting to Azure DevOps

Test results are automatically reported to Azure DevOps if configured. You can also use Azure DevOps integration directly:

```python
from api_testing.integrations import AzureDevOpsIntegration
from api_testing.core.config import Config

config = Config()
azure_config = config.get_azure_devops_config()

azure = AzureDevOpsIntegration(
    organization_url=azure_config['organization_url'],
    project=azure_config['project'],
    personal_access_token=azure_config['personal_access_token']
)

# Report test execution
test_results = [
    {
        'title': 'Test User Creation',
        'outcome': 'Passed',
        'duration_ms': 150
    },
    {
        'title': 'Test User Update',
        'outcome': 'Failed',
        'duration_ms': 200,
        'error_message': 'Validation error'
    }
]

run_id = azure.report_test_execution(
    test_name="API Test Suite",
    test_results=test_results,
    plan_id=12345  # Optional
)
```

## Project Structure

```
python-project/
├── api_testing/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── api_client.py      # REST API client
│   │   └── config.py           # Configuration management
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── jira_integration.py          # Jira integration
│   │   └── azure_devops_integration.py  # Azure DevOps integration
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api_examples.py         # Sample tests
│   └── pytest_plugin.py                 # Pytest plugin for integrations
├── .env.example                         # Example environment variables
├── config.yaml.example                  # Example YAML configuration
├── pytest.ini                           # Pytest configuration
├── requirements.txt                     # Python dependencies
├── setup.py                            # Package setup
└── README.md                           # This file
```

## Authentication Options

The API client supports multiple authentication methods:

### Bearer Token
```python
client.set_auth("bearer", token="your-token")
```

### Basic Authentication
```python
client.set_auth("basic", username="user", password="pass")
```

### API Key
```python
client.set_auth("api_key", api_key="your-key", header_name="X-API-Key")
```

## Getting Jira API Token

1. Log in to your Atlassian account
2. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
3. Click "Create API token"
4. Give it a label and copy the token

## Getting Azure DevOps PAT

1. Sign in to your Azure DevOps organization
2. Click on your profile picture → Security
3. Click "Personal access tokens" → "New Token"
4. Set the required permissions (Test Management: Read & write)
5. Copy the generated token

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.
