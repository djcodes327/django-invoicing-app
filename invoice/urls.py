from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('clients/', views.ClientsView.as_view(), name='clients'),
    path('invoices/', views.InvoicesView.as_view(), name='invoices'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('company-details/', views.CompanyProfileView.as_view(), name='company-details'),

    # Create Invoice URL Path's
    path('invoices/create/', views.CreateInvoiceView.as_view(), name='create-invoice'),
    path('invoices/create-build/<slug:slug>', views.CreateBuildInvoiceView.as_view(), name='create-build-invoice'),

]