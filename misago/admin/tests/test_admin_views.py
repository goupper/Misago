from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from misago.admin.testutils import admin_login


class AdminIndexViewTests(TestCase):
    def test_view_returns_200(self):
        """admin index view returns 200"""
        User = get_user_model()
        User.objects.create_superuser('Bob', 'bob@test.com', 'Pass.123')
        admin_login(self.client, 'Bob', 'Pass.123')

        response = self.client.get(reverse('misago:admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob', response.content)


class AdminLoginViewTests(TestCase):
    def test_login_returns_200_on_get(self):
        """unauthenticated request to admin index produces login form"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Sign in', response.content)
        self.assertIn('Username or e-mail', response.content)
        self.assertIn('Password', response.content)

    def test_login_returns_200_on_invalid_post(self):
        """form handles invalid data gracefully"""
        response = self.client.post(
            reverse('misago:admin:index'),
            data={'username': 'Nope', 'password': 'Nope'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Your login or password is incorrect.', response.content)
        self.assertIn('Sign in', response.content)
        self.assertIn('Username or e-mail', response.content)
        self.assertIn('Password', response.content)

    def test_login_returns_200_on_valid_post(self):
        """form handles valid data correctly"""
        User = get_user_model()
        User.objects.create_superuser('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:admin:index'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 302)

