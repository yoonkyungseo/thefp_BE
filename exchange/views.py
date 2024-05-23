import os
from django.core.serializers import serialize
from django.conf import settings
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
        # 'searchdate':'20240522',
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
        serializer = ExchangeRateSerializer(data=save_data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    msg = {'data':'Exchange Rate data save Success'}

    ex_rate = ExchangeRate.objects.all()
    json_data = serialize('json', ex_rate)
    file_path = os.path.join(settings.BASE_DIR, 'exchange/fixtures/exchange', 'exchange_rate.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)
        msg['json'] = 'Data has been exported to JSON file.'

    return Response(msg, status=status.HTTP_200_OK)