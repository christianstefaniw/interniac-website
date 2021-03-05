from django.test import TestCase
from django.urls import reverse


class AboutUsTestCast(TestCase):
    def test_aboutus_url(self):
        response = self.client.get(reverse('aboutus'), follow=True)
        self.assertTrue(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], reverse('aboutus'))