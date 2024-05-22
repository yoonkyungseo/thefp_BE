from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from faker import Faker
import random
from savedata.models import DepositProducts, AnnuityProducts, creditLoanProducts
from .models import User
from savedata.serializers import DepositProductsSerializer, DepositOptionsSerializer
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

def delete_user(request):
    User.objects.all().delete()
    message='성공'
    return Response(message)

@authentication_classes([TokenAuthentication])
@api_view(['GET','PUT'])
def profile(request):
    # 프로필 페이지 조회
    user = User.objects.get(username=request.user.username)
    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        products = user.product
        pro_serializer = DepositProductsSerializer(products, many=True)
        data = {
            'user':user_serializer.data,
            'product':pro_serializer.data,
        }
        return Response(data)
    # nickname 수정
    elif request.method == 'PUT':
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response(user_serializer.data)

@api_view(['GET','PUT'])
def reset_pw(request, email):
    user = User.objects.get(email=email)
    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
    if request.method == 'PUT':
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response(user_serializer.data)

@api_view(['DELETE'])
def delete_product(request, product_pk):
    # 예/적금 찜한 상품 삭제
    user = User.objects.get(username=request.user.username)
    product = user.product.get(pk=product_pk)
    product.delete()
    
    Response({'message':f"{product_pk} 상품 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)



# fake user 생성
@api_view(['GET'])
def fake_user(request):
    msg = []
    fake = Faker('ko-KR')
    for _ in range(1000):
        nickname = fake.name()
        password = fake.password(length=8, special_chars=True, upper_case=False, lower_case=True)
        email = fake.email()
        while User.objects.filter(username=email.split('@')[0]).exists():
            email = fake.email()
        birth = fake.date_between(start_date='-90y', end_date='-19y')
        gender = fake.pyint(min_value=0, max_value=1)
        crdt_grad = fake.pyint(min_value=10, max_value=999)
        salary = fake.pyint(min_value=2500, max_value=20000)
        m_consumption = fake.pyint(min_value=0, max_value=300)
        creditcard = fake.pyint(min_value=0, max_value=5)
        save_user = {
            'username':email.split('@')[0],
            'password':password,
            'nickname':nickname,
            'email':email,
            'birth':birth,
            'gender':gender,
            'crdt_grad':crdt_grad,
            'salary':salary,
            'm_consumption':m_consumption,
            'creditcard':creditcard,
        }
        serializer = UserSerializer(data = save_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            msg.append("성공")
    return Response(msg)

# @api_view(['POST'])
# def update_user_passwords(request):
#     users = User.objects.all()
#     fake_passwords = {}

#     for user in users:
#         new_password = "test_password"  # 모든 사용자에게 동일한 테스트 비밀번호를 설정
#         user.set_password(new_password)
#         user.save()
#         fake_passwords[user.username] = new_password

#     return Response(fake_passwords)

# user 모델에 fake 가입 상품 생성
@api_view(['GET'])
def fake_products(request):
    products = DepositProducts.objects.all()
    annuities = AnnuityProducts.objects.all()
    creditloans = creditLoanProducts.objects.all()

    users = User.objects.all()

    for user in users:
        if products.exists():
            selected_products = random.sample(list(products), k=random.randint(1, min(5, len(products))))
            user.product.add(*selected_products)

        if annuities.exists():
            selected_annuities = random.sample(list(annuities), k=random.randint(0, min(5, len(annuities))))
            user.annuity.add(*selected_annuities)

        if creditloans.exists():
            selected_creditloans = random.sample(list(creditloans), k=random.randint(0, min(5, len(creditloans))))
            user.creditloan.add(*selected_creditloans)
        
        user.save()
    return Response({"message": "Products, annuities, and creditloans added successfully to all users."})
