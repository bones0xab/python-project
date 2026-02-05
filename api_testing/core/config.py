"""Configuration management for the testing framework"""

import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """Configuration manager for the testing framework"""
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration
        
        Args:
            config_file: Path to YAML configuration file (optional)
        """
        # Load environment variables from .env file
        load_dotenv()
        
        self._config = {}
        
        # Load from YAML file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        
        # Override with environment variables
        self._load_env_variables()
    
    def _load_env_variables(self):
        """Load configuration from environment variables"""
        # Jira configuration
        if 'jira' not in self._config:
            self._config['jira'] = {}
        
        self._config['jira']['server'] = os.getenv('JIRA_SERVER', 
                                                    self._config.get('jira', {}).get('server', ''))
        self._config['jira']['username'] = os.getenv('JIRA_USERNAME', 
                                                      self._config.get('jira', {}).get('username', ''))
        self._config['jira']['api_token'] = os.getenv('JIRA_API_TOKEN', 
                                                       self._config.get('jira', {}).get('api_token', ''))
        self._config['jira']['project_key'] = os.getenv('JIRA_PROJECT_KEY', 
                                                         self._config.get('jira', {}).get('project_key', ''))
        
        # Azure DevOps configuration
        if 'azure_devops' not in self._config:
            self._config['azure_devops'] = {}
        
        self._config['azure_devops']['organization_url'] = os.getenv('AZURE_DEVOPS_ORG_URL', 
                                                                      self._config.get('azure_devops', {}).get('organization_url', ''))
        self._config['azure_devops']['project'] = os.getenv('AZURE_DEVOPS_PROJECT', 
                                                             self._config.get('azure_devops', {}).get('project', ''))
        self._config['azure_devops']['personal_access_token'] = os.getenv('AZURE_DEVOPS_PAT', 
                                                                           self._config.get('azure_devops', {}).get('personal_access_token', ''))
        self._config['azure_devops']['test_plan_id'] = os.getenv('AZURE_DEVOPS_TEST_PLAN_ID', 
                                                                  self._config.get('azure_devops', {}).get('test_plan_id', ''))
        
        # API configuration
        if 'api' not in self._config:
            self._config['api'] = {}
        
        self._config['api']['base_url'] = os.getenv('API_BASE_URL', 
                                                     self._config.get('api', {}).get('base_url', ''))
        self._config['api']['timeout'] = int(os.getenv('API_TIMEOUT', 
                                                        self._config.get('api', {}).get('timeout', 30)))
        self._config['api']['verify_ssl'] = os.getenv('API_VERIFY_SSL', 
                                                       str(self._config.get('api', {}).get('verify_ssl', 'true'))).lower() == 'true'
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'jira.server')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def get_jira_config(self) -> Dict[str, Any]:
        """Get Jira configuration"""
        return self._config.get('jira', {})
    
    def get_azure_devops_config(self) -> Dict[str, Any]:
        """Get Azure DevOps configuration"""
        return self._config.get('azure_devops', {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self._config.get('api', {})
