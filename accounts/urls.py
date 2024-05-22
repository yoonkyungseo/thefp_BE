from django.urls import path
from . import views

app_name='ac'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('delete_product/<int:product_pk>/', views.delete_product, name='delete_product'),
    path('reset_pw/<str:email>/', views.reset_pw, name='reset_pw'),

    
    # fake data 생성
    path('fake_user/', views.fake_user, name='fake_user'),
    path('fake_products/', views.fake_products, name='fake_products'),
    # path('update_user_passwords/', views.update_user_passwords, name='update_user_passwords'),

    # user 모델 초기화
    path('delete_user/', views.delete_user, name='delete_user')
]