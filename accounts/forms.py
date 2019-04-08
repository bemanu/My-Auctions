from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    username = forms.CharField(
        # widget=forms.TextInput(
        #     attrs={
        #         "class": "form-control",
        #         "placeholder": "user name"
        #     }
        # )
    )
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Insert a valid email address.',)
    bio = forms.CharField(max_length=254, help_text='optional. Something about you', required=False)
    birth_date = forms.DateField()
    address = forms.CharField(max_length=150, help_text='Optional. Your address', required=False)

    class Meta:
        model = User
        fields = ('username', 'bio', 'birth_date', 'address', 'email', 'password1', 'password2',)

    @property
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    @property
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already in used")
        return email


class EditProfileForm(UserChangeForm):
    bio = forms.CharField(max_length=254, help_text='optional. Something about you', required=False)
    birth_date = forms.DateField(required=False)
    address = forms.CharField(max_length=150, help_text='Optional. Your address', required=False)

    class Meta:
        model = User
        fields = ('bio', 'birth_date', 'address',  )

    def clean_password(self):
        return self.clean_password


class PasswordChangeForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password',)

