"""Sample API tests demonstrating the framework usage"""

import pytest
from api_testing.core.api_client import APIClient
from api_testing.core.config import Config


@pytest.fixture(scope="session")
def api_config():
    """Load API configuration"""
    try:
        config = Config(config_file='config.yaml')
        api_config = config.get_api_config()
        # If base_url is not configured, use default
        if not api_config.get('base_url'):
            api_config['base_url'] = 'https://jsonplaceholder.typicode.com'
        return api_config
    except:
        # Return default config if config file doesn't exist
        return {
            'base_url': 'https://jsonplaceholder.typicode.com',
            'timeout': 30,
            'verify_ssl': True
        }


@pytest.fixture(scope="session")
def api_client(api_config):
    """Create API client"""
    base_url = api_config.get('base_url', 'https://jsonplaceholder.typicode.com')
    timeout = api_config.get('timeout', 30)
    verify_ssl = api_config.get('verify_ssl', True)
    
    return APIClient(base_url=base_url, timeout=timeout, verify_ssl=verify_ssl)


@pytest.mark.api_test
class TestJSONPlaceholderAPI:
    """Sample tests using JSONPlaceholder API (public test API)"""
    
    def test_get_all_posts(self, api_client):
        """Test GET request to fetch all posts"""
        response = api_client.get('/posts')
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0
    
    def test_get_single_post(self, api_client):
        """Test GET request to fetch a single post"""
        response = api_client.get('/posts/1')
        
        assert response.status_code == 200
        post = response.json()
        assert 'id' in post
        assert 'title' in post
        assert 'body' in post
        assert post['id'] == 1
    
    def test_create_post(self, api_client):
        """Test POST request to create a new post"""
        new_post = {
            'title': 'Test Post',
            'body': 'This is a test post',
            'userId': 1
        }
        
        response = api_client.post('/posts', json=new_post)
        
        assert response.status_code == 201
        created_post = response.json()
        assert 'id' in created_post
        assert created_post['title'] == new_post['title']
    
    def test_update_post(self, api_client):
        """Test PUT request to update a post"""
        updated_post = {
            'id': 1,
            'title': 'Updated Title',
            'body': 'Updated body',
            'userId': 1
        }
        
        response = api_client.put('/posts/1', json=updated_post)
        
        assert response.status_code == 200
        result = response.json()
        assert result['title'] == updated_post['title']
    
    def test_delete_post(self, api_client):
        """Test DELETE request to delete a post"""
        response = api_client.delete('/posts/1')
        
        assert response.status_code == 200
    
    def test_get_nonexistent_post(self, api_client):
        """Test GET request for a non-existent resource"""
        response = api_client.get('/posts/99999')
        
        assert response.status_code == 404


@pytest.mark.api_test
class TestAPIHeaders:
    """Test API headers and authentication"""
    
    def test_response_headers(self, api_client):
        """Test that response includes expected headers"""
        response = api_client.get('/posts/1')
        
        assert response.status_code == 200
        assert 'content-type' in response.headers
        assert 'application/json' in response.headers['content-type']
    
    def test_custom_headers(self, api_client):
        """Test sending custom headers"""
        custom_headers = {
            'X-Custom-Header': 'test-value'
        }
        
        response = api_client.get('/posts/1', headers=custom_headers)
        
        assert response.status_code == 200


@pytest.mark.api_test
class TestAPIValidation:
    """Test API response validation"""
    
    def test_response_schema_validation(self, api_client):
        """Test that response matches expected schema"""
        response = api_client.get('/users/1')
        
        assert response.status_code == 200
        user = response.json()
        
        # Validate required fields
        required_fields = ['id', 'name', 'username', 'email']
        for field in required_fields:
            assert field in user, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(user['id'], int)
        assert isinstance(user['name'], str)
        assert isinstance(user['username'], str)
        assert isinstance(user['email'], str)
