from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Inquiry


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", max_length=150, widget=forms.EmailInput(attrs={"autocomplete": "username"})
    )

    def clean_username(self):
        return self.cleaned_data["username"].casefold()


class SignupForm(UserCreationForm):
    first_name = forms.CharField(label="Name", max_length=150, widget=forms.TextInput(attrs={"autocomplete": "name"}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    field_order = ["first_name", "email", "password1", "password2"]

    class Meta(UserCreationForm.Meta):
        fields = ["first_name", "email"]

    def clean_email(self):
        email = self.cleaned_data["email"].casefold()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account already uses this email.")
        return email

    def clean(self):
        cleaned = super().clean()
        self.instance.username = cleaned.get("email", "")
        return cleaned


class SeatForm(forms.Form):
    seats = forms.MultipleChoiceField(label="Seats", widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, labels, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["seats"].choices = [(label, label) for label in labels]

    def clean_seats(self):
        seats = sorted(set(self.cleaned_data["seats"]))
        if len(seats) > 6:
            raise forms.ValidationError("Choose between one and six seats.")
        return seats


class CheckoutForm(forms.Form):
    promo = forms.CharField(label="Offer code", max_length=20, required=False)
    gift_code = forms.UUIDField(label="Gift card code", required=False)


class GiftCardForm(forms.Form):
    recipient = forms.CharField(label="Recipient name", max_length=100)
    amount = forms.TypedChoiceField(
        label="Gift amount", coerce=int, choices=[(500, "₹500"), (1000, "₹1,000"), (1500, "₹1,500")],
    )


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class NewsletterForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    def clean_email(self):
        return self.cleaned_data["email"].lower()
