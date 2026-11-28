from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"autocomplete": "name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    class Meta(UserCreationForm.Meta):
        fields = ("name", "email", "username")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self._meta.model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account already uses this email address.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name, _, user.last_name = self.cleaned_data["name"].partition(" ")
        if commit:
            user.save()
        return user
