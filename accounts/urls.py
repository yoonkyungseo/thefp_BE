from django.urls import path
from . import views

app_name='ac'
urlpatterns = [
    # 프로필 조회
    path('profile/', views.profile, name='profile'),
    # 찜한 예/적금 상품 삭제
    path('delete_product/<int:product_pk>/', views.delete_product, name='delete_product'),
    # 비밀번호 재설정
    path('reset_pw/', views.reset_pw, name='reset_pw'),

    
    # fake data 생성
    path('fake_user/', views.fake_user, name='fake_user'),
    path('fake_products/', views.fake_products, name='fake_products'),

    # user 모델 초기화
    path('delete_user/', views.delete_user, name='delete_user')
]