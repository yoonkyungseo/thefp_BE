from django.urls import path
from . import views

app_name='savedata'
urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products, name='save_deposit'),
    path('save-annuity-products/', views.save_annuity_products, name='save_annuity'),
    path('save-creditloan-products/', views.save_creditloan_products, name='save_creditloan'),
]