from django.urls import path, include
from . import views

urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit'),
    path('save-installment-products/', views.save_installment_products, name='save_installment'),
    path('save-annuity-products/', views.save_annuity_products, name='save_annuity'),
    path('save-creditloan-products', views.save_creditloan_products, name='save_creditloan'),





    path('deposit-products/', views.deposit_products),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('deposit-products/top_rate/', views.top_rate)
]
