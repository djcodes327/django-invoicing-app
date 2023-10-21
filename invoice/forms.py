from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class DateInput(forms.DateInput):
    input_type = 'date'


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'id': 'floatingInput', 'class': 'form-control form-control-lg', 'placeholder': 'Username'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'id': 'floatingPassword', 'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
        required=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientName', 'clientLogo', 'addressLine1', 'addressLine2', 'province', 'postalCode', 'phoneNumber',
                  'emailAddress', 'taxNumber']
        widgets = {
            'clientName': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'clientLogo': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true'}),
            'addressLine1': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'addressLine2': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'province': forms.Select(attrs={'class': 'form-control', 'id': 'province-select', 'required': 'true'}),
            'postalCode': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emailAddress': forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'}),
            'taxNumber': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
        }

        labels = {
            'clientName': 'Client Name',
            'clientLogo': 'Client Logo',
            'addressLine1': 'Address Line 1',
            'addressLine2': 'Address Line 2',
            'province': 'Province',
            'postalCode': 'Postal Code',
            'phoneNumber': 'Phone Number',
            'emailAddress': 'Email Address',
            'taxNumber': 'Tax Number',
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'quantity', 'price', 'currency']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'true'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'true'}),
            'currency': forms.Select(attrs={'class': 'form-control', 'id': 'currency-select', 'required': 'true'}),
        }

        labels = {
            'title': 'Title',
            'description': 'Description',
            'quantity': 'Quantity',
            'price': 'Price',
            'currency': 'Currency',
        }


class InvoiceForm(forms.ModelForm):
    PAYMENT_TERMS = [
        ('7 Days', '7 Days'),
        ('15 Days', '15 Days'),
        ('30 Days', '30 Days'),
        ('45 Days', '45 Days'),
        ('60 Days', '60 Days'),
        ('90 Days', '90 Days'),
    ]
    INVOICE_STATUS = [
        ('DRAFT', 'DRAFT'),
        ('SENT', 'SENT'),
        ('VIEWED', 'VIEWED'),
        ('PARTIAL PAYMENT', 'PARTIAL PAYMENT'),
        ('PAID', 'PAID'),
        ('OVERDUE', 'OVERDUE'),
        ('CANCELLED', 'CANCELLED'),
    ]
    title = forms.CharField(
        required=True,
        label='Invoice Name or Title',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Invoice Title'}), )

    dueDate = forms.DateField(
        required=True,
        label='Invoice Due',
        widget=DateInput(attrs={'class': 'form-control mb-3'}), )

    paymentTerms = forms.ChoiceField(
        choices=PAYMENT_TERMS,
        required=True,
        label='Select Payment Terms',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}), )

    status = forms.ChoiceField(
        choices=INVOICE_STATUS,
        required=True,
        label='Change Invoice Status',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}), )

    notes = forms.CharField(
        required=True,
        label='Enter any notes for the client',
        widget=forms.Textarea(attrs={'class': 'form-control mb-3'}), )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6'),
                Column('dueDate', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('paymentTerms', css_class='form-group col-md-6'),
                Column('status', css_class='form-group col-md-6'),
                css_class='form-row'),
            'notes',

            Submit('submit', ' Submit ', css_class='btn bg-gradient-primary w-30'))

    class Meta:
        model = Invoice
        fields = ['title', 'dueDate', 'paymentTerms', 'status', 'notes']


# class ClientSelectForm(forms.ModelForm):
#     class Meta:
#         model = Invoice
#         fields = ['client']
#
#     def clean_client(self):
#         selected_client = self.cleaned_data['client']
#         print("Selected Client : ", selected_client)
#         if selected_client == '-----':
#             return self.initial_client
#         else:
#             return Client.objects.get(clientId=selected_client)
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         self.initial_client = kwargs.pop('initial_client')
#         self.CLIENT_LIST = Client.objects.filter(user=self.user)
#         self.CLIENT_CHOICES = [('-----', '--Select a Client--')]
#
#         for client in self.CLIENT_LIST:
#             d_t = (client.clientId, client.clientName)
#             self.CLIENT_CHOICES.append(d_t)
#
#         super(ClientSelectForm, self).__init__(*args, **kwargs)
#
#         self.fields['client'] = forms.ChoiceField(
#             label='Choose your client',
#             choices=self.CLIENT_CHOICES,
#             widget=forms.Select(attrs={'class': 'form-group form-control mb-3'}), )

class ClientSelectForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client']

    def clean_client(self):
        selected_client = self.cleaned_data['client']
        if selected_client == '-----':
            return None
        else:
            return Client.objects.get(clientId=selected_client)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.initial_client = kwargs.pop('initial_client', None)  # Handle None if initial_client is not provided
        self.CLIENT_LIST = Client.objects.filter(user=self.user)
        self.CLIENT_CHOICES = [('-----', '--Select a Client--')]

        if self.initial_client is None:
            self.initial_client = '-----'  # Set a default value when there is no initial client

        for client in self.CLIENT_LIST:
            d_t = (client.clientId, client.clientName)
            self.CLIENT_CHOICES.append(d_t)

        super(ClientSelectForm, self).__init__(*args, **kwargs)

        self.fields['client'] = forms.ChoiceField(
            label='Choose your client',
            choices=self.CLIENT_CHOICES,
            widget=forms.Select(attrs={'class': 'form-group form-control mb-3'}),
            initial=self.initial_client  # Set the initial value to the provided or default value
        )


class CompanySettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = [
            'clientName',
            'clientLogo',
            'addressLine1',
            'addressLine2',
            'province',
            'city',
            'postalCode',
            'country',
            'phoneNumber',
            'emailAddress',
            'website',
            'taxNumber',
            'notes',
            'paymentTerms',
            'creditLimit'
        ]

        widgets = {
            'clientName': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'clientLogo': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': 'true'}),
            'addressLine1': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'addressLine2': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'province': forms.Select(attrs={'class': 'form-control', 'id': 'province-select', 'required': 'true'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'postalCode': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emailAddress': forms.EmailInput(attrs={'class': 'form-control', 'required': 'true'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'required': 'true'}),
            'taxNumber': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'paymentTerms': forms.Select(
                attrs={'class': 'form-control', 'id': 'payment-terms-select', 'required': 'true'}),
            'creditLimit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

        labels = {
            'clientName': 'Client Name',
            'clientLogo': 'Client Logo',
            'addressLine1': 'Address Line 1',
            'addressLine2': 'Address Line 2',
            'province': 'Province',
            'city': 'City',
            'postalCode': 'Postal Code',
            'country': 'Country',
            'phoneNumber': 'Phone Number',
            'emailAddress': 'Email Address',
            'website': 'Website',
            'taxNumber': 'Tax Number',
            'notes': 'Notes',
            'paymentTerms': 'Payment Terms',
            'creditLimit': 'Credit Limit',
        }
