from django import forms
from django.contrib.auth.models import User

import re
import django.contrib.auth as auth

class UserLoginForm(forms.ModelForm):
    username_email = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control p_input', 'required': 'required'}),
    )

    class Meta:
        model = User
        fields = ['username_email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control p_input', 'required': 'required'}),
        }
        required = {
            'password': True
        }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        if self.is_bound and self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    existing_classes = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f"{existing_classes} is-invalid"
    
    def clean_username_email(self):
        username_email = self.cleaned_data.get('username_email', '').strip()
        username_regex = r'^[A-Za-z][A-Za-z0-9_]*$'
        email_regex = r'^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(username_regex, username_email) and not re.match(email_regex, username_email):
            raise forms.ValidationError("Please enter a valid username or email!")
        return username_email

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        password_regex = r'^\S+$'
        if not re.match(password_regex, password):
            raise forms.ValidationError("Password must not be empty or contain spaces!")
        return password

    def clean(self):
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()
        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control p_input', 'required': 'required'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'type': 'text', 'class': 'form-control p_input', 'required': 'required'}),
            'email': forms.TextInput(attrs={'type': 'text', 'class': 'form-control p_input', 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control p_input', 'required': 'required'}),
        }
        required = {
            'username': True,
            'email': True,
            'password': True,
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        if self.is_bound and self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    existing_classes = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f"{existing_classes} is-invalid"

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname', '').strip()
        fullname_regex = r'^[A-Za-z][A-Za-z\s]*$'
        if not re.match(fullname_regex, fullname):
            raise forms.ValidationError("Name must start with a letter and contain only letters and spaces!")
        return fullname
    
    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        username_regex = r'^[A-Za-z][A-Za-z0-9_]*$'
        if not re.match(username_regex, username):
            raise forms.ValidationError("Username must start with a letter and may contain letters, numbers, and underscores!")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already registered! Please use other username!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        email_regex = r'^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, email):
            raise forms.ValidationError("Please enter a valid email!")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered! Please use other email!")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password', '').strip()
        password_regex = r'^\S+$'
        if not re.match(password_regex, password):
            raise forms.ValidationError("Password must not be empty or contain spaces!")
        return password

    def clean(self):
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['fullname']
        user.set_password(self.cleaned_data['password']) # Hash password otomatis!
        if commit:
            user.save()
        return user
    
class EditProfileForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control p_input', 'required': 'required'}),
    )

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'type': 'text', 'class': 'form-control p_input', 'required': 'required'}),
        }
        required = {
            'email': True,
        }


    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['fullname'].initial = self.instance.first_name
        
        if self.is_bound and self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    existing_classes = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f"{existing_classes} is-profile-invalid"

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname', '').strip()
        fullname_regex = r'^[A-Za-z][A-Za-z\s]*$'
        if not re.match(fullname_regex, fullname):
            raise forms.ValidationError("Name must start with a letter and contain only letters and spaces!")
        return fullname

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        email_regex = r'^[A-Za-z][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, email):
            raise forms.ValidationError("Email regex not match")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already registered! Please use other email!")
        return email

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('fullname')
        
        if commit:
            user.save()
        return user

class EditPasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control p_input', 'required': 'required'}),
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control p_input', 'required': 'required'}),
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control p_input', 'required': 'required'}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditPasswordForm, self).__init__(*args, **kwargs)
        if self.is_bound and self.errors:
            for field_name, field in self.fields.items():
                if field_name in self.errors:
                    existing_classes = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f"{existing_classes} is-password-invalid"

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '').strip()
        if self.user and not self.user.check_password(old_password):
            raise forms.ValidationError("Incorrect old password!")
        return old_password

    def clean_new_password(self):
        password = self.cleaned_data.get("new_password", "").strip()
        password_regex = r'^\S+$'
        if not re.match(password_regex, password):
            raise forms.ValidationError("Password must not be empty or contain spaces!")
        return password

    def clean(self):
        cleaned_data = super().clean()
        for field, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field] = value.strip()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Password confirmation do not match!")

        return cleaned_data

    def save(self, request=None):
        new_password = self.cleaned_data.get('new_password')
        self.user.set_password(new_password)
        self.user.save()

        if request:
            auth.update_session_auth_hash(request, self.user)

        return self.user