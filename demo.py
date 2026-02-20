#!/usr/bin/env python3
"""
Simple demonstration of the REST API Testing Framework
This demo shows how to use the framework without requiring network access.
"""

from api_testing.core.api_client import APIClient
from api_testing.core.config import Config
from unittest.mock import Mock, patch

print("=" * 70)
print("REST API Testing Framework - Demo")
print("=" * 70)
print()

# 1. Demonstrate API Client Creation
print("1. Creating API Client")
print("-" * 70)
client = APIClient(
    base_url="https://api.example.com",
    timeout=30,
    verify_ssl=True
)
print(f"✓ API Client created with base_url: {client.base_url}")
print(f"  - Timeout: {client.timeout}s")
print(f"  - SSL Verification: {client.verify_ssl}")
print()

# 2. Demonstrate Authentication
print("2. Setting up Authentication")
print("-" * 70)
print("Bearer Token Authentication:")
client.set_auth("bearer", token="demo-token-123")
print(f"✓ Authorization header set: Bearer demo-token-123")
print()

print("API Key Authentication:")
client2 = APIClient(base_url="https://api.example.com")
client2.set_auth("api_key", api_key="my-api-key", header_name="X-API-Key")
print(f"✓ API Key header set: X-API-Key: my-api-key")
print()

# 3. Demonstrate Configuration
print("3. Configuration Management")
print("-" * 70)
config = Config()
print("✓ Configuration loaded")
print(f"  - Jira Server: {config.get('jira.server', 'Not configured')}")
print(f"  - Azure DevOps URL: {config.get('azure_devops.organization_url', 'Not configured')}")
print(f"  - API Base URL: {config.get('api.base_url', 'Not configured')}")
print()

# 4. Demonstrate Mock API Call
print("4. Simulated API Request (using mocks)")
print("-" * 70)
with patch('api_testing.core.api_client.requests.Session.request') as mock_request:
    # Setup mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'id': 1,
        'title': 'Test Post',
        'body': 'This is a test post',
        'userId': 1
    }
    mock_request.return_value = mock_response
    
    # Make request
    response = client.get('/posts/1')
    
    print(f"GET /posts/1")
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
print()

# 5. Show Available Integrations
print("5. Available Integrations")
print("-" * 70)
print("✓ Jira Integration")
print("  - Create test issues")
print("  - Update test results")
print("  - Link related issues")
print()
print("✓ Azure DevOps Integration")
print("  - Create test runs")
print("  - Update test results")
print("  - Complete test runs")
print()

# 6. Summary
print("=" * 70)
print("Framework Ready!")
print("=" * 70)
print()
print("Next Steps:")
print("1. Configure your credentials in .env or config.yaml")
print("2. Write your API tests in api_testing/tests/")
print("3. Run tests with: pytest")
print("4. Or use standalone runner: python run_tests.py")
print()
print("For more examples, see EXAMPLES.md")
print("For full documentation, see README.md")
print()
