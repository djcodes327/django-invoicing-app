from django import forms
from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            # Contact Information
            'address',
            'city',
            'state',
            'country',
            'postal_code',
            # About User
            'about_me',
            'date_of_birth',
            'website',
            'profile_pic',
            'cover_picture',
            # Company Details
            'role',
            'company',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'country': 'Country',
            'postal_code': 'Postal Code',
            'about_me': 'About Me',
            'date_of_birth': 'Date of Birth',
            'website': 'Website',
            'profile_pic': 'Profile Picture',
            'cover_picture': 'Cover Picture',
        }
