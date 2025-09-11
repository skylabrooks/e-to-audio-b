import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open
from credentials import get_credentials, _validate_credentials, get_project_id

class TestGetCredentials:
    @patch.dict(os.environ, {}, clear=True)
    def test_no_credentials(self):
        """Test when no credentials are available."""
        result = get_credentials()
        assert result is None

    @patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': '/fake/path.json'})
    @patch('os.path.exists')
    def test_file_not_exists(self, mock_exists):
        """Test when credential file doesn't exist."""
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError):
            get_credentials()

    @patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS': '/fake/path.json'})
    @patch('os.path.exists')
    @patch('builtins.open', mock_open(read_data='{"type": "service_account", "project_id": "test"}'))
    def test_file_credentials(self, mock_exists):
        """Test loading credentials from file."""
        mock_exists.return_value = True
        
        result = get_credentials()
        assert result is not None
        assert result['type'] == 'service_account'

    @patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS_JSON': '{"type": "service_account", "project_id": "test", "private_key": "key", "client_email": "test@test.com"}'})
    def test_json_string_credentials(self):
        """Test loading credentials from JSON string."""
        result = get_credentials()
        assert result is not None
        assert result['type'] == 'service_account'

    @patch.dict(os.environ, {
        'GOOGLE_PROJECT_ID': 'test-project',
        'GOOGLE_PRIVATE_KEY': 'test-key',
        'GOOGLE_CLIENT_EMAIL': 'test@test.com'
    })
    def test_individual_env_vars(self):
        """Test loading credentials from individual environment variables."""
        result = get_credentials()
        assert result is not None
        assert result['project_id'] == 'test-project'
        assert result['client_email'] == 'test@test.com'

    @patch.dict(os.environ, {'GOOGLE_APPLICATION_CREDENTIALS_JSON': 'invalid json'})
    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        with pytest.raises(ValueError):
            get_credentials()

class TestValidateCredentials:
    def test_valid_credentials(self):
        """Test validation of valid credentials."""
        creds = {
            'type': 'service_account',
            'project_id': 'test-project',
            'private_key': 'test-key',
            'client_email': 'test@test.com'
        }
        
        # Should not raise exception
        _validate_credentials(creds)

    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        creds = {
            'type': 'service_account',
            'project_id': 'test-project'
            # Missing private_key and client_email
        }
        
        with pytest.raises(ValueError, match="Missing required credential fields"):
            _validate_credentials(creds)

    def test_invalid_type(self):
        """Test validation with invalid credential type."""
        creds = {
            'type': 'invalid_type',
            'project_id': 'test-project',
            'private_key': 'test-key',
            'client_email': 'test@test.com'
        }
        
        with pytest.raises(ValueError, match="Invalid credential type"):
            _validate_credentials(creds)

class TestGetProjectId:
    @patch.dict(os.environ, {'GOOGLE_PROJECT_ID': 'env-project'})
    def test_from_env_var(self):
        """Test getting project ID from environment variable."""
        result = get_project_id()
        assert result == 'env-project'

    @patch.dict(os.environ, {}, clear=True)
    @patch('credentials.get_credentials')
    def test_from_credentials(self, mock_get_creds):
        """Test getting project ID from credentials."""
        mock_get_creds.return_value = {'project_id': 'creds-project'}
        
        result = get_project_id()
        assert result == 'creds-project'

    @patch.dict(os.environ, {}, clear=True)
    @patch('credentials.get_credentials')
    def test_no_project_id(self, mock_get_creds):
        """Test when no project ID is available."""
        mock_get_creds.return_value = None
        
        result = get_project_id()
        assert result is None