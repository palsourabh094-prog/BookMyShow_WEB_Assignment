from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AccountTests(TestCase):
    registration = {
        "name": "Taylor Example",
        "email": "taylor@example.com",
        "username": "taylor",
        "password1": "mango-slate-48-piano",
        "password2": "mango-slate-48-piano",
    }

    def test_signup_rejects_missing_name_invalid_email_and_mismatched_password(self):
        response = self.client.post(reverse("signup"), {
            **self.registration, "name": "", "email": "invalid", "password2": "different",
        })

        form = response.context["form"]
        for field in ("name", "email", "password2"):
            self.assertIn(field, form.errors)
        self.assertFalse(get_user_model().objects.exists())

    def test_signup_login_and_logout(self):
        response = self.client.post(reverse("signup"), self.registration, follow=True)
        self.assertContains(response, "Account created successfully.")
        user = get_user_model().objects.get(username=self.registration["username"])
        self.assertEqual(user.get_full_name(), self.registration["name"])
        self.assertTrue(user.check_password(self.registration["password1"]))
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("home"))
        self.assertNotIn(SESSION_KEY, self.client.session)

        response = self.client.post(reverse("login"), {
            "username": user.username, "password": "incorrect",
        })
        self.assertTrue(response.context["form"].non_field_errors())
        self.assertNotIn(SESSION_KEY, self.client.session)

        response = self.client.post(reverse("login"), {
            "username": user.username, "password": self.registration["password1"],
        }, follow=True)
        self.assertContains(response, "Signed in successfully.")
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    def test_account_forms_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        for route in ("signup", "login", "logout"):
            with self.subTest(route=route):
                self.assertEqual(client.post(reverse(route)).status_code, 403)
