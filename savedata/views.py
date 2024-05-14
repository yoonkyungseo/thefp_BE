from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
from django.core.validators import ProhibitNullCharactersValidator
from .serializers import DepositOptionsSerializer, DepositProductsSerializer
from .serializers import  InstallmentOptionsSerializer, InstallmentProductsSerializer
from .serializers import AnnuityOptionsSerializer, AnnuityProductsSerializer
from .serializers import creditLoanOptionSerializer, creditLoanProductSerializer

from .models import DepositOptions, DepositProducts
from django.shortcuts import get_object_or_404

API_KEY = settings.API_KEY
max_page = 6

# 예금
@api_view(['GET'])
def save_deposit_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    message = []
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000', # 은행(020000), 여신전문(030200), 저축은행(030300), 보험(050000), 금융투자(060000)
        'pageNo': 0
    }
    
    finance = ['020000', '030200', '030300', '050000', '060000']
    for fin in finance:
        params['topFinGrpNo'] = fin
        for num in range(1, max_page):
            params['pageNo'] = num
            response = requests.get(BASE_URL, params=params).json()
            #DepositProducts
            for base_list in response.get('result').get('baseList'):
                fin_prdt_cd = base_list.get('fin_prdt_cd')
                kor_co_nm = base_list.get('kor_co_nm')
                fin_prdt_nm = base_list.get('fin_prdt_nm')
                etc_note = base_list.get('etc_note')
                join_deny = base_list.get('join_deny')
                join_member = base_list.get('join_member')
                join_way = base_list.get('join_way')
                spcl_cnd = base_list.get('spcl_cnd')

                save_products = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'kor_co_nm':kor_co_nm,
                    'fin_prdt_nm':fin_prdt_nm,
                    'etc_note':etc_note,
                    'join_deny':join_deny,
                    'join_member':join_member,
                    'join_way':join_way,
                    'spcl_cnd':spcl_cnd,
                }
                serializer = DepositProductsSerializer(data=save_products)
                if serializer.is_valid(raise_exception=True):
                    product_ = serializer.save()
                    message.append("DepositProducts 성공")
            # DepositOptions
            for option_list in response.get('result').get('optionList'):
                fin_prdt_cd = option_list.get('fin_prdt_cd')
                intr_rate_type_nm = option_list.get('intr_rate_type_nm')
                intr_rate = option_list.get('intr_rate')
                intr_rate2 = option_list.get('intr_rate2')
                save_trm = option_list.get('save_trm')

                save_options = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'intr_rate_type_nm':intr_rate_type_nm,
                    'intr_rate':intr_rate,
                    'intr_rate2':intr_rate2,
                    'save_trm':save_trm,
                }
                # products = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
                serializer = DepositOptionsSerializer(data=save_options)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=product_)
                    message.append("DepositOptions 성공")
                    '''
                    data = {
                        "serializer_data":serializer.data,
                        "message":message
                    }
                    '''
    return Response(message, status=status.HTTP_201_CREATED)


# 적금
@api_view(['GET'])
def save_installment_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    message = []
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000', # 은행(020000), 여신전문(030200), 저축은행(030300), 보험(050000), 금융투자(060000)
        'pageNo': 0
    }
    
    finance = ['020000', '030200', '030300', '050000', '060000']
    for fin in finance:
        params['topFinGrpNo'] = fin
        for num in range(1, max_page):
            params['pageNo'] = num
            response = requests.get(BASE_URL, params=params).json()
            # Installment Products
            for base_list in response.get('result').get('baseList'):
                fin_prdt_cd = base_list.get('fin_prdt_cd')
                kor_co_nm = base_list.get('kor_co_nm')
                fin_prdt_nm = base_list.get('fin_prdt_nm')
                etc_note = base_list.get('etc_note')
                join_deny = base_list.get('join_deny')
                join_member = base_list.get('join_member')
                join_way = base_list.get('join_way')
                spcl_cnd = base_list.get('spcl_cnd')

                save_products = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'kor_co_nm':kor_co_nm,
                    'fin_prdt_nm':fin_prdt_nm,
                    'etc_note':etc_note,
                    'join_deny':join_deny,
                    'join_member':join_member,
                    'join_way':join_way,
                    'spcl_cnd':spcl_cnd,
                }
                serializer = InstallmentProductsSerializer(data=save_products)
                if serializer.is_valid(raise_exception=True):
                    product_ = serializer.save()
                    message.append("Installment Products 성공")
            # Installment Options
            for option_list in response.get('result').get('optionList'):
                fin_prdt_cd = option_list.get('fin_prdt_cd')
                intr_rate_type_nm = option_list.get('intr_rate_type_nm')
                intr_rate = option_list.get('intr_rate')
                intr_rate2 = option_list.get('intr_rate2')
                save_trm = option_list.get('save_trm')
                rsrv_type_nm = option_list.get('rsrv_type_nm')
                rsrv_type = option_list.get('rsrv_type')

                save_options = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'intr_rate_type_nm':intr_rate_type_nm,
                    'intr_rate':intr_rate,
                    'intr_rate2':intr_rate2,
                    'save_trm':save_trm,
                    'rsrv_type_nm':rsrv_type_nm,
                    'rsrv_type':rsrv_type,
                }
                serializer = InstallmentOptionsSerializer(data=save_options)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=product_)
                    message.append("Installment Options 성공")
    return Response(message, status=status.HTTP_201_CREATED)
        
# 연금저축
@api_view(['GET'])
def save_annuity_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/annuitySavingProductsSearch.json'
    message = []
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000', # 은행(020000), 여신전문(030200), 저축은행(030300), 보험(050000), 금융투자(060000)
        'pageNo': 0
    }
    
    finance = ['020000', '030200', '030300', '050000', '060000']
    for fin in finance:
        params['topFinGrpNo'] = fin
        for num in range(1, max_page):
            params['pageNo'] = num
            response = requests.get(BASE_URL, params=params).json()
            # Annuity Products
            for base_list in response.get('result').get('baseList'):
                fin_prdt_cd = base_list.get('fin_prdt_cd')
                kor_co_nm = base_list.get('kor_co_nm')
                fin_prdt_nm = base_list.get('fin_prdt_nm')
                etc = base_list.get('etc')
                join_way = base_list.get('join_way')
                pnsn_kind_nm = base_list.get('pnsn_kind_nm')
                mntn_cnt = base_list.get('mntn_cnt')
                prdt_type_nm = base_list.get('prdt_type_nm')
                dcls_rate = base_list.get('dcls_rate')
                guar_rate = base_list.get('guar_rate')
                btrm_prft_rate_1 = base_list.get('btrm_prft_rate_1')
                btrm_prft_rate_2 = base_list.get('btrm_prft_rate_2')
                sale_co = base_list.get('sale_co')
                dcls_strt_day = base_list.get('dcls_strt_day')
                dcls_end_day = base_list.get('dcls_end_day')

                save_products = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'kor_co_nm':kor_co_nm,
                    'fin_prdt_nm':fin_prdt_nm,
                    'etc':etc,
                    'join_way':join_way,
                    'pnsn_kind_nm':pnsn_kind_nm,
                    'mntn_cnt':mntn_cnt,
                    'prdt_type_nm':prdt_type_nm,
                    'dcls_rate':dcls_rate,
                    'guar_rate':guar_rate,
                    'btrm_prft_rate_1':btrm_prft_rate_1,
                    'btrm_prft_rate_2':btrm_prft_rate_2,
                    'sale_co':sale_co,
                    'dcls_strt_day':dcls_strt_day,
                    'dcls_end_day':dcls_end_day,
                }
                serializer = AnnuityProductsSerializer(data=save_products)
                if serializer.is_valid(raise_exception=True):
                    product_ = serializer.save()
                    message.append("Annuity Products 성공")
            # Installment Options
            for option_list in response.get('result').get('optionList'):
                fin_prdt_cd = option_list.get('fin_prdt_cd')
                pnsn_recp_trm = option_list.get('pnsn_recp_trm')
                pnsn_entr_age = option_list.get('pnsn_entr_age')
                mon_paym_atm = option_list.get('mon_paym_atm')
                paym_prd = option_list.get('paym_prd')
                pnsn_strt_age = option_list.get('pnsn_strt_age')
                pnsn_recp_amt = option_list.get('pnsn_recp_amt')

                save_options = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'pnsn_recp_trm':pnsn_recp_trm,
                    'pnsn_entr_age':pnsn_entr_age,
                    'mon_paym_atm':mon_paym_atm,
                    'paym_prd':paym_prd,
                    'pnsn_strt_age':pnsn_strt_age,
                    'pnsn_recp_amt':pnsn_recp_amt,
                }
                serializer = AnnuityOptionsSerializer(data=save_options)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=product_)
                    message.append("Annuity Options 성공")
    return Response(message, status=status.HTTP_201_CREATED)


# 개인 신용 대출
@api_view(['GET'])
def save_creditloan_products(request):
    BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/creditLoanProductsSearch.json'
    message = []
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000', # 은행(020000), 여신전문(030200), 저축은행(030300), 보험(050000), 금융투자(060000)
        'pageNo': 0
    }
    
    finance = ['020000', '030200', '030300', '050000', '060000']
    for fin in finance:
        params['topFinGrpNo'] = fin
        for num in range(1, max_page):
            params['pageNo'] = num
            response = requests.get(BASE_URL, params=params).json()
            # creditLoan Products
            for base_list in response.get('result').get('baseList'):
                fin_prdt_cd = base_list.get('fin_prdt_cd')
                kor_co_nm = base_list.get('kor_co_nm')
                fin_prdt_nm = base_list.get('fin_prdt_nm')
                join_way = base_list.get('join_way')
                crdt_prdt_type = base_list.get('crdt_prdt_type')
                crdt_prdt_type_nm = base_list.get('crdt_prdt_type_nm')
                cb_name = base_list.get('cb_name')
                dcls_strt_day = base_list.get('dcls_strt_day')
                dcls_end_day = base_list.get('dcls_end_day')

                save_products = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'kor_co_nm':kor_co_nm,
                    'fin_prdt_nm':fin_prdt_nm,
                    'join_way':join_way,
                    'crdt_prdt_type':crdt_prdt_type,
                    'crdt_prdt_type_nm':crdt_prdt_type_nm,
                    'cb_name':cb_name,
                    'dcls_strt_day':dcls_strt_day,
                    'dcls_end_day':dcls_end_day,
                }
                serializer = creditLoanProductSerializer(data=save_products)
                if serializer.is_valid(raise_exception=True):
                    product_ = serializer.save()
                    message.append("creditLoan Products 성공")
            # creditLoan Options
            for option_list in response.get('result').get('optionList'):
                crdt_lend_rate_type = option_list.get('crdt_lend_rate_type')
                crdt_lend_rate_type_nm = option_list.get('crdt_lend_rate_type_nm')
                crdt_grad_1 = option_list.get('crdt_grad_1')
                crdt_grad_4 = option_list.get('crdt_grad_4')
                crdt_grad_5 = option_list.get('crdt_grad_5')
                crdt_grad_6 = option_list.get('crdt_grad_6')
                crdt_grad_10 = option_list.get('crdt_grad_10')
                crdt_grad_11 = option_list.get('crdt_grad_11')
                crdt_grad_12 = option_list.get('crdt_grad_12')
                crdt_grad_13 = option_list.get('crdt_grad_13')
                crdt_grad_avg = option_list.get('crdt_grad_avg')

                save_options = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'crdt_lend_rate_type':crdt_lend_rate_type,
                    'crdt_lend_rate_type_nm':crdt_lend_rate_type_nm,
                    'crdt_grad_1':crdt_grad_1,
                    'crdt_grad_4':crdt_grad_4,
                    'crdt_grad_5':crdt_grad_5,
                    'crdt_grad_6':crdt_grad_6,
                    'crdt_grad_10':crdt_grad_10,
                    'crdt_grad_11':crdt_grad_11,
                    'crdt_grad_12':crdt_grad_12,
                    'crdt_grad_13':crdt_grad_13,
                    'crdt_grad_avg':crdt_grad_avg,
                }
                serializer = creditLoanOptionSerializer(data=save_options)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(product=product_)
                    message.append("creditLoan Options 성공")
    return Response(message, status=status.HTTP_201_CREATED)









@api_view(['GET','POST'])
def deposit_products(request):
    products = DepositProducts.objects.all()
    if request.method == 'GET':
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

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