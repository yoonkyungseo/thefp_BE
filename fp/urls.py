from django.urls import path, include
from . import views

urlpatterns = [
    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('deposit-products/top_rate/', views.top_rate),
    
]