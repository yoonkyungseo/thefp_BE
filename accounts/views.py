import os
from django.core.serializers import serialize
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from faker import Faker
from fp.bank_img import BANK_IMAGE_URL_DICT
import random
from savedata.models import DepositProducts, DepositOptions, AnnuityProducts, creditLoanProducts
from .models import User
from savedata.serializers import DepositProductsSerializer, DepositOptionsSerializer
from .serializers import UserSerializer
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
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
        user_info = user_serializer.data
        like_product = []
        products = user.product
        pro_serializer = DepositProductsSerializer(products, many=True)
        for product in pro_serializer.data:
            kor_co_nm = product.get('kor_co_nm')
            fin_prdt_cd = product.get('fin_prdt_cd')
            fin_co_no = product.get('fin_co_no')
            product['imgUrl'] = BANK_IMAGE_URL_DICT.get(kor_co_nm, '/assets/icons/banks/default-logo.svg')
            options = DepositOptions.objects.filter(fin_co_no=fin_co_no, fin_prdt_cd=fin_prdt_cd).order_by('-intr_rate_type_nm','-intr_rate2')[0]
            opt_serializer = DepositOptionsSerializer(options)
            product['intr_rate2'] = opt_serializer.data.get("intr_rate2")
            like_product.append(product)
        data = {
            'user': {
                'id':user_info.get('id'),
                'nickname':user_info.get('nickname'),
                'birth':user_info.get('birth'),
                'email':user_info.get('email')
            },
            'product':like_product,
        }
        return Response(data, status=status.HTTP_200_OK)
    # nickname 수정
    elif request.method == 'PUT':
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response(user_serializer.data)

# 비밀번호 찾기
@api_view(['POST','PUT'])
def reset_pw(request):
    # 이메일로 유저찾기
    if request.method == 'POST':
        user = User.objects.get(email=request.data['email'])
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    # 비밀번호 변경
    if request.method == 'PUT':
        user = User.objects.get(email=request.data.get('email'))
        data = {
            'password':make_password(request.data['password'])
        }
        user_serializer = UserSerializer(user, data=data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return Response({'message':"비밀번호 변경 완료"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_product(request, product_pk):
    # 예/적금 찜한 상품 삭제
    user = User.objects.get(username=request.user.username)
    product = user.product.filter(pk=product_pk)
    if product.exists():
        product.delete()
        msg = {'message':f"{product_pk} 상품 삭제 완료"}
    else:
        msg = {'message':f"{product_pk} 상품 없음"}
    
    return Response(msg, status=status.HTTP_200_OK)



# fake user 생성
@api_view(['GET'])
def fake_user(request):
    msg = []
    fake = Faker('ko-KR')
    for _ in range(1000):
        nickname = fake.name()
        email = fake.email()
        while User.objects.filter(username=email.split('@')[0]).exists():
            email = fake.email()
        birth = fake.date_between(start_date='-90y', end_date='-19y')
        gender = fake.pyint(min_value=0, max_value=1)
        crdt_grad = fake.pyint(min_value=10, max_value=999)
        salary = fake.pyint(min_value=1800, max_value=24000)
        m_consumption = fake.pyint(min_value=50, max_value=1000)
        asset = fake.pyint(min_value=-5000, max_value=100000)
        real_estate = fake.pyint(min_value=0, max_value=1)
        invest_tendency = fake.pyint(min_value=0, max_value=5)
        save_user = {
            'username':email.split('@')[0],
            'password':make_password("test_password"),
            'nickname':nickname,
            'email':email,
            'birth':birth,
            'gender':gender,
            'crdt_grad':crdt_grad,
            'salary':salary,
            'm_consumption':m_consumption,
            'asset':asset,
            'real_estate':real_estate,
            'invest_tendency':invest_tendency,
        }
        serializer = UserSerializer(data = save_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            msg.append("성공")
    return Response(msg, status=status.HTTP_201_CREATED)

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
        msg = {"data": "Products, annuities, and creditloans added successfully to all users."}
    
    all_user = User.objects.all()
    json_data = serialize('json', all_user)
    file_path = os.path.join(settings.BASE_DIR, 'accounts/fixtures/accounts', 'fake_user.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)
        msg['json'] = 'Data has been exported to JSON file.'

    return Response(msg, status=status.HTTP_201_CREATED)
