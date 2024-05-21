from django.urls import path
from . import views

app_name='ac'
urlpatterns = [
    path('fake_user/', views.fake_user, name='fake_user'),
    path('fake_products/', views.fake_products, name='fake_products'),
    path('delete_user/', views.delete_user, name='delete_user')
]