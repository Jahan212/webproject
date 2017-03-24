from django import forms
from django.contrib.auth import (authenticate, get_user_model, login, logout,)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user  = authenticate(username = username, password = password)
        if username and password:
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")

        return super(UserLoginForm, self).clean()

class UserSignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=128,label='First name')
    last_name = forms.CharField(max_length=128,label='last name')
    email = forms.EmailField(label='Email address')
    confirm_email = forms.EmailField(label='Confirm email')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    address_line = forms.CharField(label='Address line')
    post_code = forms.CharField(label='Post code')
    phone_number = forms.CharField(label='Contact number')
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'password',
            'confirm_password',
            'address_line',
            'post_code',
            'phone_number'
        ]

    def clean(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        address_line = self.cleaned_data.get('address_line')
        post_code = self.cleaned_data.get('post_code')
        phone_number = self.cleaned_data.get('phone_number')

        if email and confirm_email and password and address_line and post_code and phone_number:
            if email != confirm_email:
                raise forms.ValidationError("Email does not match")

            if len(password) < 8:
                raise forms.ValidationError("Password must be longer than 8 characters")

            if password != confirm_password:
                raise forms.ValidationError("Passwords must match")

            email_queryset = User.objects.filter(email=email)
            if email_queryset.count() > 0:
                raise forms.ValidationError("This email is used by another user")

            return super(UserSignUpForm, self).clean()
