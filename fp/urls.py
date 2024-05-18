from django.urls import path
from . import views

app_name = 'fp'
urlpatterns = [
    path('deposit-products/', views.deposit_products),
    path('installment-products/', views.installment_products),
    path('annuity-products/', views.annuity_products),
    path('creditLoan_products/', views.creditLoan_products),


    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
    path('deposit-products/top_rate/', views.top_rate),
    
]