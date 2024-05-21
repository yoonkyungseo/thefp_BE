from django.shortcuts import render
from rest_framework.decorators import api_view
from faker import Faker
import random
from savedata.models import DepositProducts, AnnuityProducts, creditLoanProducts
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.response import Response

def delete_user(request):
    User.objects.all().delete()
    message='성공'
    return Response(message)

# Create your views here.
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
