"""Unit tests for the API client without requiring network access"""

import pytest
from api_testing.core.api_client import APIClient
from unittest.mock import Mock, patch


class TestAPIClientUnit:
    """Unit tests for API client"""
    
    def test_api_client_initialization(self):
        """Test API client initialization"""
        client = APIClient(base_url="https://api.example.com", timeout=60)
        
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 60
        assert client.verify_ssl is True
    
    def test_api_client_base_url_normalization(self):
        """Test that trailing slash is removed from base URL"""
        client = APIClient(base_url="https://api.example.com/")
        
        assert client.base_url == "https://api.example.com"
    
    def test_set_auth_bearer(self):
        """Test setting bearer token authentication"""
        client = APIClient(base_url="https://api.example.com")
        client.set_auth("bearer", token="test-token")
        
        assert "Authorization" in client.session.headers
        assert client.session.headers["Authorization"] == "Bearer test-token"
    
    def test_set_auth_api_key(self):
        """Test setting API key authentication"""
        client = APIClient(base_url="https://api.example.com")
        client.set_auth("api_key", api_key="test-key", header_name="X-Custom-Key")
        
        assert "X-Custom-Key" in client.session.headers
        assert client.session.headers["X-Custom-Key"] == "test-key"
    
    def test_set_auth_basic(self):
        """Test setting basic authentication"""
        client = APIClient(base_url="https://api.example.com")
        client.set_auth("basic", username="user", password="pass")
        
        assert client.session.auth == ("user", "pass")
    
    @patch('api_testing.core.api_client.requests.Session.request')
    def test_get_request(self, mock_request):
        """Test GET request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response
        
        client = APIClient(base_url="https://api.example.com")
        response = client.get('/test')
        
        assert response.status_code == 200
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[0] == 'GET'
        assert args[1] == 'https://api.example.com/test'
    
    @patch('api_testing.core.api_client.requests.Session.request')
    def test_post_request(self, mock_request):
        """Test POST request"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_request.return_value = mock_response
        
        client = APIClient(base_url="https://api.example.com")
        response = client.post('/test', json={'key': 'value'})
        
        assert response.status_code == 201
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[0] == 'POST'
        assert args[1] == 'https://api.example.com/test'
        assert 'json' in kwargs
