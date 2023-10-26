from django.urls import path

from . import views

urlpatterns = [
    path('product/', views.ClientListCreateView.as_view(), name='product-list'),
    # path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(), name='product-update'),
    # path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view(), name='product-delete'),
    # path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
]
