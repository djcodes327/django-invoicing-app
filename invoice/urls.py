from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('clients/', views.ClientsView.as_view(), name='clients'),
    path('invoices/', views.InvoicesView.as_view(), name='invoices'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('company-details/', views.CompanyProfileView.as_view(), name='company-details'),

    # Create Invoice URL Path's
    path('create/', views.CreateInvoiceView.as_view(), name='create-invoice'),
    path('create-build/<slug:slug>', views.CreateBuildInvoiceView.as_view(), name='create-build-invoice'),

    # PDF and Document Invoice View's
    path('view-pdf/<slug:slug>', views.PDFInvoiceView.as_view(), name='view-pdf-invoice'),
    path('view-document/<slug:slug>', views.DocumentInvoiceView.as_view(), name='view-document-invoice'),

    # Delete View's
    path('client/<slug:slug>/delete/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('invoice/<slug:slug>/delete/', views.InvoiceDeleteView.as_view(), name='invoice-delete'),
    path('product/<slug:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
]
