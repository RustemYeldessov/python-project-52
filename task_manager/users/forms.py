from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy

User = get_user_model()

class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        required=True,
        label=gettext_lazy("Password"),
        widget=forms.PasswordInput,
        help_text=gettext_lazy("Your password must contain at least 3 characters.")
    )
    password2 = forms.CharField(
        required=True,
        label=gettext_lazy("Confirm Password"),
        widget=forms.PasswordInput,
        help_text=gettext_lazy("Enter the same password again for verification.")
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]
        labels = {
            'first_name': gettext_lazy('First name'),
            'last_name': gettext_lazy('Last name'),
            'username': gettext_lazy('Username'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'username': forms.TextInput(attrs={'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", gettext_lazy("Passwords do not match."))

            if len(password1) < 3:
                self.add_error(
                    "password2",
                    gettext_lazy("The entered password is too short. \
                        It must contain at least 3 characters."),
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label=gettext_lazy('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=gettext_lazy("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )