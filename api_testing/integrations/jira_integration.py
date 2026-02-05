"""Jira integration for reporting test results"""

import logging
from typing import Dict, Any, Optional
from jira import JIRA
from jira.exceptions import JIRAError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JiraIntegration:
    """Integration with Jira for test result reporting"""
    
    def __init__(self, server: str, username: str, api_token: str, project_key: str):
        """
        Initialize Jira integration
        
        Args:
            server: Jira server URL
            username: Jira username/email
            api_token: Jira API token
            project_key: Jira project key
        """
        self.server = server
        self.username = username
        self.api_token = api_token
        self.project_key = project_key
        
        try:
            self.jira = JIRA(
                server=server,
                basic_auth=(username, api_token)
            )
            logger.info(f"Connected to Jira server: {server}")
        except JIRAError as e:
            logger.error(f"Failed to connect to Jira: {str(e)}")
            raise
    
    def create_test_issue(self, summary: str, description: str, 
                         issue_type: str = "Test", **kwargs) -> Optional[str]:
        """
        Create a test issue in Jira
        
        Args:
            summary: Issue summary
            description: Issue description
            issue_type: Issue type (default: Test)
            **kwargs: Additional fields
            
        Returns:
            Issue key if successful, None otherwise
        """
        try:
            issue_dict = {
                'project': {'key': self.project_key},
                'summary': summary,
                'description': description,
                'issuetype': {'name': issue_type},
            }
            
            # Add any additional fields
            issue_dict.update(kwargs)
            
            issue = self.jira.create_issue(fields=issue_dict)
            logger.info(f"Created Jira issue: {issue.key}")
            return issue.key
        except JIRAError as e:
            logger.error(f"Failed to create Jira issue: {str(e)}")
            return None
    
    def update_test_result(self, issue_key: str, status: str, 
                          comment: Optional[str] = None) -> bool:
        """
        Update test result in Jira
        
        Args:
            issue_key: Jira issue key
            status: Test status (Pass/Fail)
            comment: Optional comment
            
        Returns:
            True if successful, False otherwise
        """
        try:
            issue = self.jira.issue(issue_key)
            
            if comment:
                self.jira.add_comment(issue, comment)
            
            # Add label for test status
            current_labels = issue.fields.labels
            status_label = f"test-{status.lower()}"
            
            if status_label not in current_labels:
                current_labels.append(status_label)
                issue.update(fields={'labels': current_labels})
            
            logger.info(f"Updated Jira issue {issue_key} with status: {status}")
            return True
        except JIRAError as e:
            logger.error(f"Failed to update Jira issue: {str(e)}")
            return False
    
    def create_test_execution_issue(self, test_cases: list, 
                                    execution_summary: str) -> Optional[str]:
        """
        Create a test execution issue to track multiple test cases
        
        Args:
            test_cases: List of test case information
            execution_summary: Summary of the test execution
            
        Returns:
            Issue key if successful, None otherwise
        """
        description = f"{execution_summary}\n\n"
        description += "Test Cases:\n"
        
        for idx, test in enumerate(test_cases, 1):
            status = test.get('status', 'Unknown')
            name = test.get('name', 'Unnamed Test')
            description += f"{idx}. {name} - {status}\n"
        
        return self.create_test_issue(
            summary=f"Test Execution: {execution_summary}",
            description=description,
            issue_type="Test Execution"
        )
    
    def link_issues(self, issue_key: str, related_issue_key: str, 
                   link_type: str = "Relates") -> bool:
        """
        Link two issues together
        
        Args:
            issue_key: First issue key
            related_issue_key: Second issue key
            link_type: Type of link (Relates, Blocks, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.jira.create_issue_link(
                type=link_type,
                inwardIssue=issue_key,
                outwardIssue=related_issue_key
            )
            logger.info(f"Linked {issue_key} to {related_issue_key}")
            return True
        except JIRAError as e:
            logger.error(f"Failed to link issues: {str(e)}")
            return False
