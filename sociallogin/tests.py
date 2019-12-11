from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse

from note.models import Notes
from .models import SocialLogin

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_URL = os.getenv('BASE_URL')


class ModelsTest(TestCase):
    fixtures = ['fundoonotes']

    def test_social_string_representation1(self):
        social = SocialLogin(provider="github", username="mdhussain7")
        self.assertEqual(str(social), "github mdhussain7")

    def test_social_string_representation2(self):
        social = SocialLogin(username="mdhussain7")
        self.assertEqual(str(social), " mdhussain7")

    def test_social_verbose_name_plural1(self):
        self.assertEqual(str(SocialLogin._meta.verbose_name_plural), "Login users")

    def test_social_verbose_name_plural2(self):
        self.assertEqual(str(SocialLogin._meta.verbose_name), "Login user")

    def test_social_verbose_name_plural3(self):
        self.assertNotEqual(str(SocialLogin._meta.verbose_name_plural), "Login user")

    def test_social_verbose_name_plural4(self):
        self.assertNotEqual(str(SocialLogin._meta.verbose_name), "Login users")

    def test_social_equal1(self):
        social1 = SocialLogin(username="My Note")
        social2 = SocialLogin(username="My NOte")
        self.assertTrue(social1 == social2, True)

    def test_social_equal2(self):
        social1 = SocialLogin(username="1 note")
        social2 = SocialLogin(username="2 note ")
        self.assertFalse(social1 == social2, True)


class SocialTest(TestCase):
    fixtures = ['fundoo']

    def test_social_getall1(self):
        url = BASE_URL + reverse('github')
        resp = self.client.get(url, content_type='application/json', )
        self.assertEqual(resp.status_code, 302)

    def test_social_getall2(self):
        url = BASE_URL + reverse('oauth')
        resp = self.client.get(url, content_type='application/json', )
        self.assertEqual(resp.status_code, 404)
