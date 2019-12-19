from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
import re,io
from PIL import Image
from fundoo.settings import BASE_URL
import json
import requests

with open("Test.json") as f:
    data = json.load(f)


class TestReg:
    def test_reg1(self):
        url = BASE_URL + '/registration/'
        file = data[0]['Test_case1']
        response = requests.post(url=url, data=file)
        assert response.status_code == 400


class Testlogin:
    def test_log1(self):
        url = BASE_URL + '/login/'
        file = data[0]['Test_case2']

        response = requests.post(url=url, data=file)
        assert response.status_code == 400


class UserTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='me', email='me@gmail.com', password='me123')
        self.user2 = User.objects.create(username='you', email='yougamil.com', password='you123')

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('users')
        data = {'username': 'md', 'email': 'mdhussainsabhussain@gmail.com', 'password': 'Ammi@786'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_get_all_user(self):
        """Test the api can we get a all users."""
        response = self.client.get(
            reverse('users', ), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_given_user(self):
        """Test the api can we get user with given id ."""
        response = self.client.get(
            reverse('users_details', kwargs={'pk': self.user1.pk}), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """
        Ensure we can update existing user object.
        """
        data = {"username": 'hussain', "email": 'srmsa786@gmail.com', "password": 'Ammi@Thammu@786'}
        response = self.client.put(reverse('users_details', kwargs={'pk': self.user1.pk}), data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_note(self):
        """
        Ensure we can delete existing object.
        """
        response = self.client.delete(reverse('users_details', kwargs={'pk': self.user1.pk}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_registration(self):
        """
        Ensure if new user can register with email verification
        """
        email = "mdhussainsabhussain@gmail.com"
        EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        result = re.match(EMAIL_REGEX, email)
        if result == None:
            raise Exception('email validation error')
        else:
            url = reverse('register')
            data = {'username': 'user', 'email': email, 'password': 'Ammi@786'}
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        """
        Ensure if authorized user able to reset the password with register email-id
        """
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email': 'test@gmail.com'}

        data = {'email': 'test@gmail.com',
                'password1': 'secret',
                'password2': 'secret'}

        User.objects.create_user(**self.credentials)
        url = reverse('reset_password')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        """
        send login data  and check it should be logged in.
        """
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
        url = reverse('login')
        response = self.client.post(url, self.credentials, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_image_file(self):

        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_upload_file(self):
        """
        test Api create user profile and upload image on aws-s3
        """
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

        url = reverse('upload_file')
        photo_file = self.create_image_file()
        data = {'image': photo_file, 'user': self.credentials['username']}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
