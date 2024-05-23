import os
from django.core.serializers import serialize
from django.conf import settings
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import DepositOptionsSerializer, DepositProductsSerializer
from .serializers import AnnuityOptionsSerializer, AnnuityProductsSerializer
from .serializers import creditLoanOptionsSerializer, creditLoanProductsSerializer
from .savemodel import save_DepositProducts, save_AnnuityProduct, save_LoanProduct, save_LoanOptions
from .models import DepositProducts, AnnuityProducts, creditLoanProducts 
from .models import DepositOptions, AnnuityOptions, creditLoanOptions
from django.core.exceptions import ObjectDoesNotExist

API_KEY = settings.API_KEY
max_page = 10

# 예금
@api_view(['GET'])
def save_deposit_products(request):
    depo_BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
    inst_BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
    for_BASE_URL = [depo_BASE_URL, inst_BASE_URL]
    for_product_type = ["예금", "적금"]
    message = []
    params = {
        'auth': API_KEY,
        'topFinGrpNo': '020000', # 은행(020000), 여신전문(030200), 저축은행(030300), 보험(050000), 금융투자(060000)
        'pageNo': 0
    }
    
    finance = ['020000', '030200', '030300', '050000', '060000']
    for product_type, BASE_URL in zip(for_product_type, for_BASE_URL):
        for fin in finance:
            params['topFinGrpNo'] = fin
            for num in range(1, max_page):
                params['pageNo'] = num
                response = requests.get(BASE_URL, params=params).json()
                #DepositProducts
                for base_list in response.get('result').get('baseList'):
                    fin_prdt_cd = base_list.get('fin_prdt_cd')
                    kor_co_nm = base_list.get('kor_co_nm')
                    fin_co_no = base_list.get('fin_co_no')
                    fin_prdt_nm = base_list.get('fin_prdt_nm')
                    etc_note = base_list.get('etc_note')
                    join_deny = base_list.get('join_deny')
                    join_member = base_list.get('join_member')
                    join_way = base_list.get('join_way')
                    spcl_cnd = base_list.get('spcl_cnd')
                    if DepositProducts.objects.filter(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no).exists():
                        continue
                    save_products = {
                        'fin_prdt_cd':fin_prdt_cd,
                        'kor_co_nm':kor_co_nm,
                        'fin_co_no':fin_co_no,
                        'fin_prdt_nm':fin_prdt_nm,
                        'etc_note':etc_note,
                        'join_deny':join_deny,
                        'join_member':join_member,
                        'join_way':join_way,
                        'spcl_cnd':spcl_cnd,
                        'product_type':product_type
                    }
                    save_DepositProducts(save_products)
                    serializer = DepositProductsSerializer(data=save_products)
                    try:
                        serializer.is_valid()
                        serializer.save()
                        message.append("DepositProducts 성공")
                    except AssertionError:
                        pass
                # DepositOptions
                for option_list in response.get('result').get('optionList'):
                    fin_prdt_cd = option_list.get('fin_prdt_cd')
                    fin_co_no = option_list.get('fin_co_no')
                    intr_rate_type_nm = option_list.get('intr_rate_type_nm')
                    intr_rate = option_list.get('intr_rate')
                    intr_rate2 = option_list.get('intr_rate2')
                    save_trm = option_list.get('save_trm')
                    rsrv_type_nm = option_list.get('rsrv_type_nm', None)
                    rsrv_type = option_list.get('rsrv_type', None)

                    save_options = {
                        'fin_prdt_cd':fin_prdt_cd,
                        'fin_co_no':fin_co_no,
                        'intr_rate_type_nm':intr_rate_type_nm,
                        'intr_rate':intr_rate,
                        'intr_rate2':intr_rate2,
                        'save_trm':save_trm,
                        'rsrv_type_nm':rsrv_type_nm,
                        'rsrv_type':rsrv_type,
                    }
                    serializer = DepositOptionsSerializer(data=save_options)
                    try:
                        product_ = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no)
                        serializer.is_valid()
                        # print(serializer.errors)
                        serializer.save(product=product_)
                        message.append("DepositOptions 성공")
                    except AssertionError:
                        pass
                    except UnboundLocalError:
                        pass
                    except ObjectDoesNotExist:
                        pass
                        '''
                        data = {
                            "serializer_data":serializer.data,
                            "message":message
                        }
                        '''
    dep_products = DepositProducts.objects.all()
    json_data = serialize('json', dep_products)
    file_path = os.path.join(settings.BASE_DIR, 'savedata/fixtures/savedata', 'deposit_products.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)

    dep_options = DepositOptions.objects.all()
    json_data = serialize('json', dep_options)
    file_path = os.path.join(settings.BASE_DIR, 'savedata/fixtures/savedata', 'deposit_options.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)

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
                fin_co_no = base_list.get('fin_co_no')
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
                if AnnuityProducts.objects.filter(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no).exists():
                        continue
                save_products = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'kor_co_nm':kor_co_nm,
                    'fin_co_no':fin_co_no,
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
                save_AnnuityProduct(save_products)
                serializer = AnnuityProductsSerializer(data=save_products)
                try:
                    serializer.is_valid()
                    serializer.save()
                    message.append("Annuity Products 성공")
                except AssertionError:
                    pass
            # Installment Options
            for option_list in response.get('result').get('optionList'):
                fin_prdt_cd = option_list.get('fin_prdt_cd')
                fin_co_no = option_list.get('fin_co_no')
                pnsn_recp_trm = option_list.get('pnsn_recp_trm')
                pnsn_entr_age = option_list.get('pnsn_entr_age')
                mon_paym_atm = option_list.get('mon_paym_atm')
                paym_prd = option_list.get('paym_prd')
                pnsn_strt_age = option_list.get('pnsn_strt_age')
                pnsn_recp_amt = option_list.get('pnsn_recp_amt')

                if pnsn_recp_amt == None:
                    pnsn_recp_amt = 0

                save_options = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'fin_co_no':fin_co_no,
                    'pnsn_recp_trm':pnsn_recp_trm,
                    'pnsn_entr_age':pnsn_entr_age,
                    'mon_paym_atm':mon_paym_atm,
                    'paym_prd':paym_prd,
                    'pnsn_strt_age':pnsn_strt_age,
                    'pnsn_recp_amt':pnsn_recp_amt,
                }
                serializer = AnnuityOptionsSerializer(data=save_options)
                try:
                    product_ = AnnuityProducts.objects.get(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no)
                    serializer.is_valid()
                    # print(serializer.errors)
                    serializer.save(product=product_)
                    message.append("Annuity Options 성공")
                except AssertionError:
                    pass
                except UnboundLocalError:
                    pass
                except ObjectDoesNotExist:
                    pass

    ann_products = AnnuityProducts.objects.all()
    json_data = serialize('json', ann_products)
    file_path = os.path.join(settings.BASE_DIR, 'savedata/fixtures/savedata', 'annuity_products.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)

    ann_options = AnnuityOptions.objects.all()
    json_data = serialize('json', ann_options)
    file_path = os.path.join(settings.BASE_DIR, 'savedata/fixtures/savedata', 'annuity_options.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)
        
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
                fin_co_no = base_list.get('fin_co_no')
                fin_prdt_nm = base_list.get('fin_prdt_nm')
                join_way = base_list.get('join_way')
                crdt_prdt_type = base_list.get('crdt_prdt_type')
                crdt_prdt_type_nm = base_list.get('crdt_prdt_type_nm')
                cb_name = base_list.get('cb_name')
                dcls_strt_day = base_list.get('dcls_strt_day')
                dcls_end_day = base_list.get('dcls_end_day')
                if creditLoanProducts.objects.filter(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no).exists():
                        continue
                save_products = {
                    'fin_prdt_cd':fin_prdt_cd,
                    'kor_co_nm':kor_co_nm,
                    'fin_co_no':fin_co_no,
                    'fin_prdt_nm':fin_prdt_nm,
                    'join_way':join_way,
                    'crdt_prdt_type':crdt_prdt_type,
                    'crdt_prdt_type_nm':crdt_prdt_type_nm,
                    'cb_name':cb_name,
                    'dcls_strt_day':dcls_strt_day,
                    'dcls_end_day':dcls_end_day,
                }
                save_LoanProduct(save_products)
                serializer = creditLoanProductsSerializer(data=save_products)
                try:
                    serializer.is_valid()
                    serializer.save()
                    message.append("creditLoan Products 성공")
                except AssertionError:
                    pass
            # creditLoan Options
            for option_list in response.get('result').get('optionList'):
                fin_prdt_cd = option_list.get('fin_prdt_cd')
                fin_co_no = option_list.get('fin_co_no')
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
                    'fin_co_no':fin_co_no,
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
                save_LoanOptions(save_options)
                serializer = creditLoanOptionsSerializer(data=save_options)
                try:
                    product_ = creditLoanProducts.objects.get(fin_prdt_cd=fin_prdt_cd, fin_co_no=fin_co_no)
                    serializer.is_valid()
                    # print(serializer.errors)
                    serializer.save(product=product_)
                    message.append("creditLoan Options 성공")
                except AssertionError:
                    pass
                except UnboundLocalError:
                    pass
                except ObjectDoesNotExist:
                    pass
    
    cre_products = creditLoanProducts.objects.all()
    json_data = serialize('json', cre_products)
    file_path = os.path.join(settings.BASE_DIR, 'savedata/fixtures/savedata', 'creditloan_products.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)

    cre_options = creditLoanOptions.objects.all()
    json_data = serialize('json', cre_options)
    file_path = os.path.join(settings.BASE_DIR, 'savedata/fixtures/savedata', 'creditloan_options.json')

    #fixtures 디렉토리가 없는 경우 생성
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # JSON 데이터를 파일로 저장
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_data)
        
    return Response(message, status=status.HTTP_201_CREATED)