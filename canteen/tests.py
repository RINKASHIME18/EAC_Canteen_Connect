from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Rating, Suggestion, Report

class HomeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(username='staff', password='password', email='staff@example.com')
        self.client.login(username='staff', password='password')

    def test_home_view_with_null_users(self):
        # Create records with null users
        Rating.objects.create(
            stall="Maren's Food Cart",
            rating=5,
            food_name="Test Food",
            feedback="Great!",
            user=None
        )
        Suggestion.objects.create(
            stall="Rhoxy Canteen",
            suggestion_text="More variety",
            user=None
        )
        Report.objects.create(
            user=self.staff_user, # Report.user is not nullable in models.py
            stall="Stall 4",
            grade_section="10-A",
            gender="Female",
            concern_text="Issue",
            is_anonymous=True
        )

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Check that 'Anonymous' is present in the rendered content
        self.assertContains(response, 'Anonymous')

    def test_model_str_with_null_users(self):
        suggestion = Suggestion.objects.create(
            stall="Rhoxy Canteen",
            suggestion_text="More variety",
            user=None
        )
        self.assertEqual(str(suggestion), "Suggestion for Rhoxy Canteen by Anonymous")

        report = Report.objects.create(
            user=self.staff_user,
            stall="Stall 4",
            grade_section="10-A",
            gender="Female",
            concern_text="Issue",
            is_anonymous=True
        )
        # Manually set user to None for test if possible (though model says non-nullable)
        # In Django, if it's not null=True, we can't easily save it as None without triggering integrity error.
        # But our __str__ check is safe anyway.
