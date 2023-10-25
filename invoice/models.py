from django.db import models
from uuid import uuid4

from django.urls import reverse

from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Client(models.Model):
    """Client model."""

    PROVINCES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Bihar', 'Bihar'),
        ('Gujarat', 'Gujarat'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Punjab', 'Punjab'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('West Bengal', 'West Bengal'),
        ('Delhi', 'Delhi'),
    ]

    PAYMENT_TERMS = [
        ('7 Days', '7 Days'),
        ('15 Days', '15 Days'),
        ('30 Days', '30 Days'),
        ('45 Days', '45 Days'),
        ('60 Days', '60 Days'),
        ('90 Days', '90 Days'),
    ]

    # Basic Fields
    clientName = models.CharField(max_length=200, null=True, blank=True)
    clientLogo = models.ImageField(default='default_logo.png', upload_to='company_logos')
    addressLine1 = models.CharField(max_length=200, null=True, blank=True)
    addressLine2 = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    postalCode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phoneNumber = models.CharField(max_length=200, null=True, blank=True)
    emailAddress = models.EmailField(null=True, blank=True)

    # Additional Fields
    website = models.URLField(max_length=200, null=True, blank=True)
    taxNumber = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Financial Information
    paymentTerms = models.CharField(max_length=20, choices=PAYMENT_TERMS, null=True, blank=True)
    creditLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Related Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    # Utility Fields
    clientId = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clientName} {self.clientId}"

    def get_absolute_url(self):
        return reverse('client-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.clientId is None:
            self.clientId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.clientName, self.clientId))

        self.slug = slugify('{} {}'.format(self.clientName, self.clientId))
        super(Client, self).save(*args, **kwargs)


class Invoice(models.Model):
    """Invoice model"""
    PAYMENT_TERMS = [
        ('7 Days', '7 Days'),
        ('15 Days', '15 Days'),
        ('30 Days', '30 Days'),
        ('45 Days', '45 Days'),
        ('60 Days', '60 Days'),
        ('90 Days', '90 Days'),  # For user-defined payment terms
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

    title = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    dueDate = models.DateField(null=True, blank=True)
    paymentTerms = models.CharField(choices=PAYMENT_TERMS, default='14 Days', max_length=20)
    status = models.CharField(choices=INVOICE_STATUS, default='CURRENT', max_length=25)
    notes = models.TextField(null=True, blank=True)

    # Related Fields/Models
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    # Utility Fields
    invoiceId = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.number} {self.invoiceId}"

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.invoiceId is None:
            self.invoiceId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.number, self.invoiceId))

        self.slug = slugify('{} {}'.format(self.number, self.invoiceId))
        super(Invoice, self).save(*args, **kwargs)


class Product(models.Model):
    """Product model."""
    CURRENCY = [
        ('USD', '$ - US Dollar'),
        ('EUR', '€ - Euro'),
        ('GBP', '£ - British Pound'),
        ('JPY', '¥ - Japanese Yen'),
        ('ILS', '₪ - Israeli New Shekel'),
        ('INR', '₹ - Indian Rupee'),
        ('RUB', '₽ - Russian Ruble'),
        ('KRW', '₩ - South Korean Won'),
        ('THB', '฿ - Thai Baht'),
        ('PHP', '₱ - Philippine Peso'),
        ('CHF', '₣ - Swiss Franc'),
    ]

    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    currency = models.CharField(max_length=100, choices=CURRENCY, default='INR', blank=True, null=True)

    # Related Fields
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    # Utility Fields
    productId = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.productId}"

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    def calculate_total_price(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if self.productId is None:
            self.productId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.title, self.productId))

        self.slug = slugify('{} {}'.format(self.title, self.productId))
        super(Product, self).save(*args, **kwargs)


class UserSettings(models.Model):
    """User Settings model."""

    PROVINCES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Bihar', 'Bihar'),
        ('Gujarat', 'Gujarat'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Punjab', 'Punjab'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('West Bengal', 'West Bengal'),
        ('Delhi', 'Delhi'),
    ]

    PAYMENT_TERMS = [
        ('7 Days', '7 Days'),
        ('15 Days', '15 Days'),
        ('30 Days', '30 Days'),
        ('45 Days', '45 Days'),
        ('60 Days', '60 Days'),
        ('90 Days', '90 Days'),
    ]
    # Basic Fields
    clientName = models.CharField(max_length=200, null=True, blank=True)
    clientLogo = models.ImageField(default='default_logo.png', upload_to='company_logos')
    addressLine1 = models.CharField(max_length=200, null=True, blank=True)
    addressLine2 = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    postalCode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    phoneNumber = models.CharField(max_length=200, null=True, blank=True)
    emailAddress = models.EmailField(null=True, blank=True)

    # Additional Fields
    website = models.URLField(max_length=200, null=True, blank=True)
    taxNumber = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Financial Information
    paymentTerms = models.CharField(choices=PAYMENT_TERMS, null=True, blank=True, max_length=50)
    creditLimit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Related Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Utility Fields
    uniqueId = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)

    # Time Stamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Settings"  # Singular display name
        verbose_name_plural = "Company Settings"  # Plural display name

    def __str__(self):
        return f"{self.clientName} {self.uniqueId}"

    def get_absolute_url(self):
        return reverse('user-settings-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.clientName, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.clientName, self.uniqueId))
        super(UserSettings, self).save(*args, **kwargs)


