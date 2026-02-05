"""Core API client for making REST API calls"""

import requests
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    """Generic REST API client for testing purposes"""
    
    def __init__(self, base_url: str, timeout: int = 30, verify_ssl: bool = True):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        
    def set_auth(self, auth_type: str, **kwargs):
        """
        Set authentication for API requests
        
        Args:
            auth_type: Type of authentication (basic, bearer, api_key)
            **kwargs: Authentication parameters
        """
        if auth_type == "basic":
            self.session.auth = (kwargs.get('username'), kwargs.get('password'))
        elif auth_type == "bearer":
            self.session.headers.update({
                'Authorization': f"Bearer {kwargs.get('token')}"
            })
        elif auth_type == "api_key":
            header_name = kwargs.get('header_name', 'X-API-Key')
            self.session.headers.update({
                header_name: kwargs.get('api_key')
            })
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (will be appended to base_url)
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Set defaults
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('verify', self.verify_ssl)
        
        logger.info(f"Making {method} request to {url}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"Response status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make a GET request"""
        return self.request('GET', endpoint, params=params, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make a POST request"""
        return self.request('POST', endpoint, data=data, json=json, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make a PUT request"""
        return self.request('PUT', endpoint, data=data, json=json, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a DELETE request"""
        return self.request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None, json: Optional[Dict] = None, **kwargs) -> requests.Response:
        """Make a PATCH request"""
        return self.request('PATCH', endpoint, data=data, json=json, **kwargs)
