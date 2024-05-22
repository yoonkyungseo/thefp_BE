from django.urls import path
from . import views

app_name='ac'
urlpatterns = [
    
    # fake data 생성
    path('fake_user/', views.fake_user, name='fake_user'),
    path('fake_products/', views.fake_products, name='fake_products'),

    # user 모델 초기화
    path('delete_user/', views.delete_user, name='delete_user')
]