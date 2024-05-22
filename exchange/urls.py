from django.urls import path
from . import views

app_name='exchange'
urlpatterns = [
    # 환율 정보 저장
    path('save_exchange_rate/', views.save_exchange_rate, name='save_exchange_rate'),
]