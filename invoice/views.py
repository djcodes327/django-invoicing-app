from uuid import uuid4

import pdfkit
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView

from customuser.forms import CustomUserForm
from .forms import UserLoginForm, ClientForm, InvoiceForm, ProductForm, ClientSelectForm, CompanySettingsForm
from .models import Client, Invoice, Product, UserSettings


# Create your views here.

class Index(View):
    """Main Index view."""

    def get(self, request, *args, **kwargs):
        return render(request, 'invoice/index.html')


class LoginView(UserPassesTestMixin, TemplateView):
    """Login View."""
    template_name = 'invoice/sign-in.html'

    def test_func(self):
        # Check if user is anonymous or not.
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        # If user is not anonymous then redirect to below path.
        return redirect(reverse_lazy('dashboard'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == 'POST':
            context['form'] = UserLoginForm(self.request.POST)
        else:
            context['form'] = UserLoginForm()

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        # Get username and password from the request/submitted form
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print(remember_me)
            if remember_me == "on":
                request.session.set_expiry(1209600)  # 2 weeks (in seconds)
            auth.login(request, user)
            return redirect('dashboard')

        else:
            print("Invalid User Credentials")
            messages.error(request, 'Invalid User Credentials')
            return redirect('login')


class RegisterView(UserPassesTestMixin, TemplateView):
    """Register View."""
    template_name = 'invoice/sign-up.html'

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        return redirect(reverse_lazy('dashboard'))

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context=context)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view."""
    template_name = 'invoice/dashboard.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Dashboard"
        return render(request, self.template_name, context=context)


class ClientsView(LoginRequiredMixin, TemplateView):
    """Clients view."""
    template_name = 'invoice/clients.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClientForm()
        context['clients'] = Client.objects.filter(user=self.request.user)
        context['page_title'] = "Clients"
        return context

    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.user = self.request.user
            new_client.save()

            messages.success(request, "New Client Added")
            return redirect('clients')
        else:
            messages.error(request, "Problem Processing your request")
            return redirect('clients')


class InvoicesView(LoginRequiredMixin, TemplateView):
    """Invoice's view."""
    template_name = 'invoice/invoices.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.filter(user=self.request.user)
        context = {
            "page_title": "Invoices",
            "invoices": invoices,
        }
        return render(request, self.template_name, context)


class ProductsView(LoginRequiredMixin, View):
    """Product's view."""
    template_name = 'invoice/products.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(user=self.request.user)
        context = {
            "page_title": "Products",
            "invoices": products,
        }
        return render(request, self.template_name, context)


class CreateInvoiceView(View):
    """Create Invoice's view.

    --> Creating an Invoice
    --> Redirecting to CreateBuildInvoiceView
    --> This ensured the product's added have an invoice associated with them.
    """

    def get(self, request, *args, **kwargs):
        # Creating a blank invoice
        number = 'INV-' + str(uuid4()).split('-')[1]
        print("Invoice Number : ", number)
        new_invoice = Invoice.objects.create(number=number)
        new_invoice.save()
        # Fetching the created invoice
        inv = Invoice.objects.get(number=number)
        return redirect('create-build-invoice', slug=inv.slug)


class CreateBuildInvoiceView(View):
    """Create Build Invoice View"""
    template_name = 'invoice/create-invoice.html'

    def get_context_data(self, slug):
        context = {}
        try:
            # Getting the invoice by the slug passed in URL
            invoice = Invoice.objects.get(slug=slug)
        except Invoice.DoesNotExist:
            # If invoice doesn't exist
            messages.error(self.request, 'Something went wrong')
            return redirect('invoices')

        # Get Products by Invoice
        products = Product.objects.filter(invoice=invoice)
        # Initialize Product Form
        prod_form = ProductForm()
        # Initial invoice form with Current Invoice Data.
        inv_form = InvoiceForm(instance=invoice)
        # Initialize Client form with current user data.
        client_form = ClientSelectForm(user=self.request.user,
                                       initial_client=invoice.client.clientId if invoice.client else None)

        context['page_title'] = 'Create Invoice'
        context['invoice'] = invoice
        context['products'] = products
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        context['client_form'] = client_form

        return context

    def get(self, request, slug):
        context = self.get_context_data(slug)
        return render(request, self.template_name, context)

    def post(self, request, slug):
        context = self.get_context_data(slug)
        prod_form = ProductForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=context['invoice'])
        client_form = ClientSelectForm(self.request.user, request.POST,
                                       initial_client=context['invoice'].client.clientId if context[
                                           'invoice'].client else None,
                                       instance=context['invoice'])

        if 'product-submit' in request.POST and prod_form.is_valid():
            product_form = prod_form.save(commit=False)
            product_form.invoice = context['invoice']
            product_form.save()
            messages.success(request, "Product added successfully")
            return redirect('create-build-invoice', slug=slug)

        elif 'invoice-submit' in request.POST and inv_form.is_valid() and 'paymentTerms' in request.POST:
            inv_form.save()
            messages.success(request, "Invoice updated successfully")
            return redirect('create-build-invoice', slug=slug)

        # Client form is now submitted with a different prefix, so check for that
        elif 'client-submit' in request.POST and client_form.is_valid() and 'client' in request.POST:
            client_form.save()
            messages.success(request, "Client added to invoice successfully")
            return redirect('create-build-invoice', slug=slug)

        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            # context['client_form'] = client_form
            messages.error(request, "Problem processing your request")
            return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, View):
    """
    User Profile View.
    """
    template_name = 'invoice/profile.html'

    def get(self, request):
        user = self.request.user
        user_form = CustomUserForm(instance=user)

        context = {
            "page_title": "Profile",
            "user": user,
            "user_form": user_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = self.request.user
        user_form = CustomUserForm(request.POST, request.FILES, instance=user)
        print("Post Data : ", request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')

        context = {
            "page_title": "Profile",
            "user": user,
            "user_form": user_form,
        }
        return render(request, self.template_name, context)


class CompanyProfileView(LoginRequiredMixin, View):
    """
    Company Profile View.
    """
    template_name = 'invoice/company-details.html'

    def get(self, request):
        user = self.request.user
        # Check if a UserSettings instance exists for the user
        try:
            user_settings = UserSettings.objects.get(user=user)
        except UserSettings.DoesNotExist:
            # If it doesn't exist, create a new instance and associate it with the user
            user_settings = UserSettings(user=user)
            user_settings.save()  # Make sure to save the new instance

        company_form = CompanySettingsForm(instance=user_settings)

        context = {
            "page_title": "Company Profile",
            "user": user,
            "company": user_settings,
            "company_form": company_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = self.request.user
        try:
            user_settings = UserSettings.objects.get(user=user)
        except UserSettings.DoesNotExist:
            user_settings = UserSettings(user=user)

        company_form = CompanySettingsForm(request.POST, request.FILES, instance=user_settings)

        if company_form.is_valid():
            company_form.save()
            return redirect('company-details')

        # If the form is not valid, handle the form errors
        context = {
            "page_title": "Profile",
            "user": user,
            "company": user_settings,
            "company_form": company_form,
        }
        return render(request, self.template_name, context)


class PDFInvoiceView(DetailView):
    model = Invoice
    template_name = 'invoice/invoice-templates.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all the products related to this invoice
        products = Product.objects.filter(invoice=self.object)

        # Get Client Settings (adjust the filter criteria as needed)
        user_company_details = UserSettings.objects.get(user=self.request.user)

        # Calculate the Invoice Total
        invoice_currency = ''
        invoice_total = 0.0

        if products:
            for product in products:
                total_price = float(product.quantity) * float(product.price)
                invoice_total += total_price
                invoice_currency = product.currency

        # context['invoice'] = self.object
        context['products'] = products
        context['company_settings'] = user_company_details
        context['invoiceTotal'] = "{:.2f}".format(invoice_total)
        context['invoiceCurrency'] = invoice_currency

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.error(request, 'Something went wrong')
            return redirect('invoices')
        return super().get(request, *args, **kwargs)


class DocumentInvoiceView(DetailView):
    model = Invoice
    template_name = 'invoice/pdf-template.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all the products related to this invoice
        products = Product.objects.filter(invoice=self.object)

        # Get Client Settings (adjust the filter criteria as needed)
        user_company_details = UserSettings.objects.get(user=self.request.user)

        # Calculate the Invoice Total
        invoice_currency = ''
        invoice_total = 0.0

        if products:
            for product in products:
                total_price = float(product.quantity) * float(product.price)
                invoice_total += total_price
                invoice_currency = product.currency

        context['products'] = products
        context['company_settings'] = user_company_details
        context['invoiceTotal'] = "{:.2f}".format(invoice_total)
        context['invoiceCurrency'] = invoice_currency

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            messages.error(request, 'Something went wrong')
            return redirect('invoices')
        return super().get(request, *args, **kwargs)

    def render_to_response(self, context):
        # The name of your PDF file
        filename = '{}.pdf'.format(self.object.invoiceId)

        # HTML File to be converted to PDF - inside your Django directory
        template = get_template(self.template_name)

        # Render the HTML
        html = template.render(context)

        # Options - Important Step!
        options = {
            'encoding': 'UTF-8',
            'javascript-delay': '1000',  # Optional
            'enable-local-file-access': None,  # To be able to access CSS
            'page-size': 'A4',
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
        }

        path_to_wkhtmltopdf = r'D:\Development\PyCharmProjects\htmltopdf\wkhtmltopdf\bin\wkhtmltopdf.exe'

        # Remember the location of wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

        # IF you have CSS to add to the template
        # css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
        # css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')

        # Create the file
        file_content = pdfkit.from_string(html, False, configuration=config, options=options, verbose=True)

        # Create the HTTP Response
        response = HttpResponse(file_content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename = {}'.format(filename)

        return response
