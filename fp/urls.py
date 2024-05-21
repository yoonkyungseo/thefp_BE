from django.urls import path
from . import views

app_name = 'fp'
urlpatterns = [
    # 상품조회
    path('deposit-products/', views.deposit_products),
    path('annuity-products/', views.annuity_products),
    path('creditLoan_products/', views.creditLoan_products),

    # 상품 상세조회
    path('deposit-product-options/<int:pk>/', views.deposit_product_options),
    path('annuity-product-options/<int:pk>/', views.annuity_product_options),
    path('creditloan-product-options/<int:pk>/', views.creditLoan_product_options),



    path('deposit-products/top_rate/', views.top_rate),
    
]