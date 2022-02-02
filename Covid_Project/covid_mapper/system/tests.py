from django.test import TestCase
from rest_framework import status
from rest_framework.test import RequestsClient
from django.core import mail
from django.db import models

# Create your tests here.
from system.models import List
from system.models import Location
from system.models import ListLocation


class UserSignUpTests(TestCase):
    """
    Tests the user register/sign up functionality
    """
    
    token = ''
    client = RequestsClient()

    # test for a valid registration
    def test_sign_in(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'test.py', 'email': 'test.py@gmail.com','password1': 'test.pyDJANGO123', 'password2': 'test.pyDJANGO123'})
        self.token = response.json().get("key")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # test for if fields are left blank
    def test_fail_sign_up_blank_fields(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'blankPassword', 'email': 'blankPassword@gmail.com','password1': 'blankPassword', 'password2': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post("http://localhost:8000/account/register/", {'username': '', 'email': 'blankUser@gmail.com','password1': 'blankUser', 'password2': 'blankUser'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post("http://localhost:8000/account/register/", {'username': 'blankEmail', 'email': '','password1': 'blankEmail', 'password2': 'blankEmail'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test for if fields passwords don't match
    def test_fail_sign_up_passwords_dont_match(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'testUser', 'email': 'testUser@gmail.com','password1': 'testUserPassword', 'password2': 'testUserPasswordDoesntMatch'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test for if fields are taken by another user
    def test_fail_sign_up_taken(self):
        # first sign up
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'testUser', 'email': 'testUser@gmail.com','password1': 'testUserPassword', 'password2': 'testUserPassword'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # failed sign up
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'testUser', 'email': 'testUserEmail@gmail.com','password1': 'testUserPassword', 'password2': 'testUserPassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post("http://localhost:8000/account/register/", {'username': 'testUser2', 'email': 'testUser@gmail.com','password1': 'testUserPassword', 'password2': 'testUserPassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserEmailConfirmationTests(TestCase):
    """
    Tests the email confirmation functionality
    """

    client = RequestsClient()
    
    def email_verification_view(self):
        response = self.client.post("http://localhost:8000/account/verification/email/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"detail": "Verification email sent"})

    # Valid sign in with email sent
    def test_email_successful_register(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'test.py', 'email': 'test.py@gmail.com','password1': 'test.pyDJANGO123', 'password2': 'test.pyDJANGO123'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[example.com] Please Confirm Your E-mail Address')
    
    # Invalid sign in with no email sent
    def test_email_unsuccessful_register(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': '', 'email': '','password1': '', 'password2': ''})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

class UserLoginTests(TestCase):
    """
    Tests the login functionality and user permissions before and after login
    """

    token = ''
    client = RequestsClient()

    # Set up valid sign in with valid auth token
    def setUp(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'test.py', 'email': 'test.py@gmail.com','password1': 'test.pyDJANGO123', 'password2': 'test.pyDJANGO123'})
        self.token = response.json().get("key")

    # test for successful login and check if auth token is the same as the one received on register
    def test_access_guest_user(self):
        self.client = RequestsClient()

        ## Guest user does not have access to
        response = self.client.get("http://localhost:8000/account/user/current/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get("http://localhost:8000/account/user/listLocations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post("http://localhost:8000/account/user/listLocations/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        ## Guest user has access to
        response = self.client.post("http://localhost:8000/account/register/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("username"), ['This field is required.'])

        response = self.client.post("http://localhost:8000/account/login/")
        self.assertEqual(response.json().get("password"), ['This field is required.'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # test for successful login and check if auth token is the same as the one received on register
    def test_log_in(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/login/", {'username': 'test.py', 'password': 'test.pyDJANGO123'})
        self.assertEqual(self.token, response.json().get("key"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.headers.update({'Authorization': 'Token %s' % self.token})
        
        # Testing views.py
        response = self.client.get("http://localhost:8000/account/user/current/")
        self.assertEqual(1, response.json().get("user_id"))

    # test for failed login if credientials aren't in database
    def test_fail_log_in(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/login/", {'username': 'unknownUser', 'password': 'unknownPassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_log_out(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': 'Successfully logged out.'})


class ListTests(TestCase):
    """
    Tests the functionality for adding a List and a Location for a logged in user
    """
    token = ''
    user_id = -1
    client = RequestsClient()

    second_token = ''
    second_user_id = -1
    second_client = RequestsClient()

    def setUp(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'testUser1', 'email': 'testUser1@gmail.com','password1': 'testUser1DJANGO123', 'password2': 'testUser1DJANGO123'})
        self.token = response.json().get("key")

        response = self.client.post("http://localhost:8000/account/login/", {'username': 'testUser1', 'password': 'testUser1DJANGO123'})
        self.client.headers.update({'Authorization': 'Token %s' % self.token})

        response = self.client.get("http://localhost:8000/account/user/current/")
        self.user_id = response.json().get("user_id")
        
        # Register and login with second user on another client
        self.second_client = RequestsClient()
        response = self.second_client.post("http://localhost:8000/account/register/", {'username': 'testUser2', 'email': 'testUser2@gmail.com','password1': 'testUser2DJANGO123', 'password2': 'testUser2DJANGO123'})
        self.second_token = response.json().get("key")

        response = self.second_client.post("http://localhost:8000/account/login/", {'username': 'testUser2', 'password': 'testUser2DJANGO123'})
        self.second_client.headers.update({'Authorization': 'Token %s' % self.second_token})

        response = self.second_client.get("http://localhost:8000/account/user/current/")
        self.second_user_id = response.json().get("user_id")
    
    # Tests that lists are added using API endpoint as well as the database
    def test_add_list(self):
        response = self.client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.json())

        response = self.client.post("http://localhost:8000/account/user/lists/", {'list_name': 'myFirstList', 'user': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('myFirstList', response.json().get("list_name"))
        self.assertEqual(self.user_id, response.json().get("user"))

        response = self.client.post("http://localhost:8000/account/user/lists/", {'list_name': 'mySecondList', 'user': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('mySecondList', response.json().get("list_name"))
        self.assertEqual(self.user_id, response.json().get("user"))

        response = self.client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.json()))
        self.assertEqual('myFirstList', response.json()[0].get("list_name"))
        self.assertEqual('mySecondList', response.json()[1].get("list_name"))

        count = List.objects.all().count()
        self.assertEqual(count, 2)
        self.assertEqual(List.objects.get(pk=1).list_name, 'myFirstList')
        self.assertEqual(List.objects.get(pk=2).list_name, 'mySecondList')
        self.assertEqual(List.objects.get(pk=1).user.id, self.user_id)
        self.assertEqual(List.objects.get(pk=2).user.id, self.user_id)

    # Test filtering lists with list_name
    def test_search_list(self):
        response = self.client.get("http://localhost:8000/account/user/lists/?list_name=" + "nonExistingList")
        self.assertEqual(len(response.json()), 0)

        response = self.client.post("http://localhost:8000/account/user/lists/", {'list_name': 'myFirstList', 'user': self.user_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("http://localhost:8000/account/user/lists/?list_name=" + "myFirstList")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get("list_name"), "myFirstList")
        self.assertEqual(response.json()[0].get("list_id"), self.user_id)

    # Test that lists are assigned to the right users
    def test_lists_multiple_users(self):
        self.client.post("http://localhost:8000/account/user/lists/", {'list_name': 'User1 list', 'user': self.user_id})
        self.second_client.post("http://localhost:8000/account/user/lists/", {'list_name': 'User2 list', 'user': self.second_user_id})
        self.second_client.post("http://localhost:8000/account/user/lists/", {'list_name': 'User2 second list', 'user': self.second_user_id})
        
        response = self.client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('list_name'), "User1 list")
        
        response = self.second_client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0].get('list_name'), "User2 list")
        self.assertEqual(response.json()[1].get('list_name'), "User2 second list")

    #Test that lists are still there after logging out and logging back in
    def test_lists_logged_out(self):

        self.client.post("http://localhost:8000/account/user/lists/", {'list_name': 'User1 list', 'user': self.user_id})
        response = self.client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('list_name'), "User1 list")

        #Log out
        response = self.client.post("http://localhost:8000/account/logout/")
        self.client.headers.clear()

        #Log back in
        response = self.client.post("http://localhost:8000/account/login/", {'username': 'testUser1', 'password': 'testUser1DJANGO123'})
        self.token = response.json().get("key")
        self.client.headers.update({'Authorization': 'Token %s' % self.token})
  
        response = self.client.get("http://localhost:8000/account/user/lists/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('list_name'), "User1 list")


class LocationTests(TestCase):
    token = ''
    user_id = -1
    client = RequestsClient()

    second_token = ''
    second_user_id = -1
    second_client = RequestsClient()

    def setUp(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'testUser1', 'email': 'testUser1@gmail.com','password1': 'testUser1DJANGO123', 'password2': 'testUser1DJANGO123'})
        self.token = response.json().get("key")

        response = self.client.post("http://localhost:8000/account/login/", {'username': 'testUser1', 'password': 'testUser1DJANGO123'})
        self.client.headers.update({'Authorization': 'Token %s' % self.token})

        response = self.client.get("http://localhost:8000/account/user/current/")
        self.user_id = response.json().get("user_id")
        
        # Register and login with second user on another client
        self.second_client = RequestsClient()
        response = self.second_client.post("http://localhost:8000/account/register/", {'username': 'testUser2', 'email': 'testUser2@gmail.com','password1': 'testUser2DJANGO123', 'password2': 'testUser2DJANGO123'})
        self.second_token = response.json().get("key")

        response = self.second_client.post("http://localhost:8000/account/login/", {'username': 'testUser2', 'password': 'testUser2DJANGO123'})
        self.second_client.headers.update({'Authorization': 'Token %s' % self.second_token})

        response = self.second_client.get("http://localhost:8000/account/user/current/")
        self.second_user_id = response.json().get("user_id")
    
    # Tests that locations are added using API endpoint as well as the database
    def test_add_locations(self):
        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([], response.json())

        response = self.client.post("http://localhost:8000/account/user/locations/",  {'street': '1 Sydney Street, Sydney 2000 NSW'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('1 Sydney Street, Sydney 2000 NSW', response.json().get("street"))

        response = self.client.post("http://localhost:8000/account/user/locations/",  {'street': '2 Sydney Street, Sydney 2000 NSW'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('2 Sydney Street, Sydney 2000 NSW', response.json().get("street"))

        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.json()))
        self.assertEqual('1 Sydney Street, Sydney 2000 NSW', response.json()[0].get("street"))
        self.assertEqual('2 Sydney Street, Sydney 2000 NSW', response.json()[1].get("street"))

        count = Location.objects.all().count()
        self.assertEqual(count, 2)
        self.assertEqual(Location.objects.get(pk=1).street, '1 Sydney Street, Sydney 2000 NSW')
        self.assertEqual(Location.objects.get(pk=2).street, '2 Sydney Street, Sydney 2000 NSW')


    # Test filtering locations with street
    def test_search_locations(self):
        response = self.client.get("http://localhost:8000/account/user/locations/?street=" + "nonExistingLocation")
        self.assertEqual(len(response.json()), 0)

        response = self.client.post("http://localhost:8000/account/user/locations/", {'street': '1 Sydney Street, Sydney 2000 NSW'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get("http://localhost:8000/account/user/locations/?street=" + '1 Sydney Street, Sydney 2000 NSW')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get("street"), "1 Sydney Street, Sydney 2000 NSW")

    # Test that locations accessable for all users
    def test_locations_multiple_users(self):
        self.client.post("http://localhost:8000/account/user/locations/", {'street': '1 Sydney Street, Sydney 2000 NSW'})
        
        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('street'), "1 Sydney Street, Sydney 2000 NSW")
        
        self.second_client.post("http://localhost:8000/account/user/locations/", {'street': '4 Sydney Street, Sydney 2000 NSW'})
        self.second_client.post("http://localhost:8000/account/user/locations/", {'street': '5 Sydney Street, Sydney 2000 NSW'})

        response = self.second_client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0].get('street'), "1 Sydney Street, Sydney 2000 NSW")
        self.assertEqual(response.json()[1].get('street'), "4 Sydney Street, Sydney 2000 NSW")
        self.assertEqual(response.json()[2].get('street'), "5 Sydney Street, Sydney 2000 NSW")

        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(response.json()[0].get('street'), "1 Sydney Street, Sydney 2000 NSW")
        self.assertEqual(response.json()[1].get('street'), "4 Sydney Street, Sydney 2000 NSW")
        self.assertEqual(response.json()[2].get('street'), "5 Sydney Street, Sydney 2000 NSW")

    #Test that locations are still there after logging out and logging back in
    def test_locations_logged_out(self):

        self.client.post("http://localhost:8000/account/user/locations/", {'street': 'The University of Sydney, Camperdown 2007 NSW'})
        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('street'), 'The University of Sydney, Camperdown 2007 NSW')

        #Log out
        response = self.client.post("http://localhost:8000/account/logout/")
        self.client.headers.clear()

        #Log back in
        response = self.client.post("http://localhost:8000/account/login/", {'username': 'testUser1', 'password': 'testUser1DJANGO123'})
        self.token = response.json().get("key")
        self.client.headers.update({'Authorization': 'Token %s' % self.token})
  
        response = self.client.get("http://localhost:8000/account/user/locations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('street'), 'The University of Sydney, Camperdown 2007 NSW')

class ListLocationTests(TestCase):
    """
    Tests the functionality for matching a list and a location a logged in user
    """
    token = ''
    user_id = -1
    client = RequestsClient()

    def setUp(self):
        self.client = RequestsClient()
        response = self.client.post("http://localhost:8000/account/register/", {'username': 'test.py', 'email': 'test.py@gmail.com','password1': 'test.pyDJANGO123', 'password2': 'test.pyDJANGO123'})
        self.token = response.json().get("key")

        response = self.client.post("http://localhost:8000/account/login/", {'username': 'test.py', 'password': 'test.pyDJANGO123'})
        self.client.headers.update({'Authorization': 'Token %s' % self.token})

        # Testing views.py
        response = self.client.get("http://localhost:8000/account/user/current/")
        self.user_id = response.json().get("user_id")

        # Add some Lists and Locations
        self.client.post("http://localhost:8000/account/user/locations/", {'street': 'Woolworths'})
        self.client.post("http://localhost:8000/account/user/locations/", {'street': 'University of Sydney'})

        self.client.post("http://localhost:8000/account/user/lists/", {'list_name': "bob's list", 'user': self.user_id})
        self.client.post("http://localhost:8000/account/user/lists/", {'list_name': "groceries", 'user': self.user_id})


    def test_add_listLocation(self):
        response = self.client.post("http://localhost:8000/account/user/listLocations/", {'list': 1, 'location': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("list"), 1)
        self.assertEqual(response.json().get("location"), 1)

        response = self.client.post("http://localhost:8000/account/user/listLocations/", {'list': 1, 'location': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("list"), 1)
        self.assertEqual(response.json().get("location"), 2)

        response = self.client.post("http://localhost:8000/account/user/listLocations/", {'list': 2, 'location': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get("list"), 2)
        self.assertEqual(response.json().get("location"), 2)

        count = ListLocation.objects.all().count()
        self.assertEqual(count, 3)
        self.assertEqual(ListLocation.objects.filter(list=1)[0].location.location_id, 1)
        self.assertEqual(ListLocation.objects.filter(list=1)[1].location.location_id, 2)
        self.assertEqual(ListLocation.objects.get(list=2).location.location_id, 2)

    def test_add_nonexistent_pk(self):
        response = self.client.post("http://localhost:8000/account/user/listLocations/", {'list': 7, 'location': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("list"), ['Invalid pk "7" - object does not exist.'])

        response = self.client.post("http://localhost:8000/account/user/listLocations/", {'list': 1, 'location': 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("location"), ['Invalid pk "10" - object does not exist.'])
