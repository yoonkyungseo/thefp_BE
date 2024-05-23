from django.shortcuts import render
from rest_framework.decorators import api_view
from django.conf import settings
import requests
from rest_framework.response import Response
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from rest_framework import status

EXCHANGE_API_KEY = settings.EXCHANGE_API_KEY
# 환율 조회
@api_view(['GET'])
def exchange_rate(request):
    ex_rate = ExchangeRate.objects.all()
    ex_serializer = ExchangeRateSerializer(ex_rate, many=True)
    data = {
        "exchange_rate":ex_serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)



# 환율 데이터 저장
@api_view(['GET'])
def save_exchange_rate(request):

    BASE_URL = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': EXCHANGE_API_KEY,
        'searchdate':'20240522',
        'data':'AP01'  # AP01: 환율, AP02: 대출금리, AP03: 국제금리
    }
    response = requests.get(BASE_URL, params=params).json()
    # Exchange rate
    for res in response:
        cur_unit = res.get('cur_unit')
        cur_nm = res.get('cur_nm')
        ttb = res.get('ttb')
        tts = res.get('tts')
        deal_bas_r = res.get('deal_bas_r')
        kftc_deal_bas_r = res.get('kftc_deal_bas_r')

        save_data = {
            'cur_unit':cur_unit,
            'cur_nm':cur_nm,
            'ttb':ttb,
            'tts':tts,
            'deal_bas_r':deal_bas_r,
            'kftc_deal_bas_r':kftc_deal_bas_r,
        }
        print(save_data)
        serializer = ExchangeRateSerializer(data=save_data)
        
        if serializer.is_valid(raise_exception=True):
            print('=====================================================')
            serializer.save()
    msg = {'message':'Exchange Rate data save Success'}
    return Response(msg, status=status.HTTP_200_OK)