"""
TEsts for the Django admin modifications.
"""


from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    """Tests for Django admin."""

    # private-test-method : Camel pattern!, I dont know why
    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='admin'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='user123',
            name='Test User'
        )

    def test_user_list(self):
        """Test that users are listed on page."""
        # Reversing admin URLs -> get full url from admin/core/user/...
        # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        # https://docs.djangoproject.com/en/3.2/topics/testing/tools/#overview-and-a-quick-example
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page work."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
