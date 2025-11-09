from django import forms
from django.contrib.auth.models import User

import re

class UserForm(forms.ModelForm):
    fullname = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['fullname', 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        username_regex = r'^[A-Za-z][A-Za-z0-9_]*$'
        if not re.match(username_regex, username):
            raise forms.ValidationError("Username regex not match")
        # Check uniqueness in the database
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already registered! Please use other username")
        return username

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname', '').strip()
        fullname_regex = r'^[A-Za-z][A-Za-z\s]*$'
        if not re.match(fullname_regex, fullname):
            raise forms.ValidationError("Fullname regex not match")
        return fullname

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        email_regex = r'^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, email):
            raise forms.ValidationError("Email regex not match")
        # Check uniqueness in the database
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered! Please use other email")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        password_regex = r'^\S+$'
        if not re.match(password_regex, password):
            raise forms.ValidationError("Password regex not match")
        return password

    def clean(self):
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()
        return cleaned_data
    
class EditFullNameForm(forms.Form):
    fullname = forms.CharField(
        max_length=150,
        required=True,
        label="Full Name",
    )

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname', '').strip()
        fullname_regex = r'^[A-Za-z][A-Za-z\s]*$'
        if not re.match(fullname_regex, fullname):
            raise forms.ValidationError("Full name regex not match (letters and spaces only)")
        return fullname

class EditPasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Old Password",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="New Password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Confirm Password",
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '').strip()
        if self.user and not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect")
        return old_password

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password", "").strip()
        # Same regex as UserForm
        password_regex = r'^\S+$'
        if not re.match(password_regex, password):
            raise forms.ValidationError("Password regex not match (no spaces allowed)")
        return password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
