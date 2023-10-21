from django.contrib import admin
from .models import Client, Invoice, Product, UserSettings


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ['clientName', 'emailAddress', 'phoneNumber', 'created_at', 'updated_at']
    search_fields = ['clientName', 'emailAddress', 'phoneNumber']
    fieldsets = (
        ('Basic Information', {
            'fields': ('clientName', 'clientLogo', 'emailAddress', 'phoneNumber', 'user'),
        }),
        ('Address Information', {
            'fields': ('addressLine1', 'addressLine2', 'city', 'province', 'postalCode', 'country'),
            'classes': ('wide',),
        }),
        ('Financial Information', {
            'fields': ('taxNumber', 'paymentTerms', 'creditLimit'),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('extrapretty',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse', 'vTimeField'),  # Use 'collapse' class to hide this section initially
        }),
    )
    list_filter = ['province', ]
    readonly_fields = ('created_at', 'updated_at')


class InvoiceAdmin(admin.ModelAdmin):
    # Get Client Name
    def client_name(self, obj):
        if obj.client:
            return obj.client.clientName
        return ''

    client_name.short_description = 'Client Name'

    list_display = ['title', 'number', 'client_name', 'dueDate', 'paymentTerms', 'status', 'created_at',
                    'updated_at']
    search_fields = ['title', 'number', 'client__clientName']
    list_filter = ['paymentTerms', 'status']
    readonly_fields = ('created_at', 'updated_at', 'slug', 'invoiceId')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'number', 'dueDate', 'paymentTerms', 'status'),
        }),
        ('Notes', {
            'fields': ('notes',),
        }),
        ('Related Fields', {
            'fields': ('client',),
        }),
        ('Unique Fields', {
            'fields': ('slug', 'invoiceId',),
        }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'quantity', 'price', 'currency', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'invoice__title']
    list_filter = ['currency']
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'quantity', 'price', 'currency'),
        }),
        ('Related Fields', {
            'fields': ('invoice',),
        }),
        ('Time Stamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Client, ClientAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserSettings)
