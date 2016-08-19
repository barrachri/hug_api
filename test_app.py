# Stdlib imports
import os
# 3rd party lib imports
import hug
import pytest
# Local imports
import app
import settings
from utils import Token

token = Token(settings.KEY)

def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    os.remove(settings.TEST_APP_DB)

class TestApp():
    def test_answer(self):
        """Test if the main url works corretly"""
        response = hug.test.get(app, '/')
        assert '404' in response.status

    def test_create_user(self):
        """Test if the creation of a new user works corretly"""
        # post data
        data = dict(email='test@test.com', password='test', blog="blog.test.io",
                    first_name="Test First Name", last_name="Test Last Name")
        response = hug.test.post(app, '/v1/users/create', **data)
        assert '200' in response.status

    def test_create_user_existing(self):
        """Test if given an existing user it returns the right error"""
        # post data
        data = dict(email='test@test.com', password='test', blog="blog.test.io",
                    first_name="Test First Name", last_name="Test Last Name")
        response = hug.test.post(app, '/v1/users/create', **data)
        assert '400' in response.status

    def test_login_user(self):
        """Test if given a valid user it returns a valid token"""
        # get data
        data = dict(email='test@test.com', password='test')
        response = hug.test.get(app, '/v1/users/login', **data).data
        assert token(response['data']['token'])

    def test_get_info_user(self):
        "Test if given a valid user it return the right token and the info about that user"
        # get data
        data = dict(email='test@test.com', password='test')
        login_response = hug.test.get(app, '/v1/users/login', **data).data
        token = login_response['data']['token']
        response = hug.test.get(app, '/v1/users', headers={'Authorization': '{}'.format(token)})
        assert '200' in response.status

    def test_update_info_user(self):
        """Test if given a valid user it returns a valid token and updates the info correctly"""
        # get data
        data = dict(email='test@test.com', password='test')
        login_response = hug.test.get(app, '/v1/users/login', **data).data
        token = login_response['data']['token']
        data = dict(email='new@new.com', password='new', blog="new.test.io",
                    first_name="New First Name", last_name="New Last Name")
        response = hug.test.put(app, '/v1/users', headers={'Authorization': '{}'.format(token), **data})
        assert '200' in response.status
