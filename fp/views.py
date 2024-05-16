from savedata.serializers import DepositOptionsSerializer, DepositProductsSerializer
from savedata.serializers import  InstallmentOptionsSerializer, InstallmentProductsSerializer
from savedata.serializers import AnnuityOptionsSerializer, AnnuityProductsSerializer
from savedata.serializers import creditLoanOptionsSerializer, creditLoanProductsSerializer
from savedata.models import DepositOptions, DepositProducts

from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests

# Create your views here.
@api_view(['GET','POST'])
def deposit_products(request):
    products = DepositProducts.objects.all()
    if request.method == 'GET':
        pro_serializer = DepositProductsSerializer(products, many=True)
        for product in products:
            options = product.deposit_option.all()
            print(options)
        opt_serializer = DepositOptionsSerializer(options)
        data ={
            'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
            'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
            'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
            'intr_rate2':opt_serializer.data.get('intr_rate2'),
            'save_trm':opt_serializer.data.get('save_trm')
        }
        return Response(data)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    products = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    opt_serializer = DepositOptionsSerializer(options, many=True)
    pro_serializer = DepositProductsSerializer(products)
    data={
        'product':pro_serializer.data,
        'options':opt_serializer.data,
    }
    return Response(data)

@api_view(['GET'])
def top_rate(request):
    options = DepositOptions.objects.order_by('-intr_rate2')[0]
    products = options.product
    product_serializer = DepositProductsSerializer(products)
    option_serializer = DepositOptionsSerializer(options)
    data ={
        'product_serializer':product_serializer.data,
        'option_serializer':option_serializer.data,
    }
    return Response(data)