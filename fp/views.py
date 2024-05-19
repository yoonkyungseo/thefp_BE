from savedata.serializers import DepositOptionsSerializer, DepositProductsSerializer
from savedata.serializers import  InstallmentOptionsSerializer, InstallmentProductsSerializer
from savedata.serializers import AnnuityOptionsSerializer, AnnuityProductsSerializer
from savedata.serializers import creditLoanOptionsSerializer, creditLoanProductsSerializer
from savedata.models import DepositOptions, DepositProducts
from savedata.models import InstallmentOptions, InstallmentProducts
from savedata.models import AnnuityOptions, AnnuityProducts
from savedata.models import creditLoanOptions, creditLoanProducts

from django.db.models import Q
from django.utils import timezone
import pytz
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
import requests

# 예금 조회
@api_view(['GET'])
def deposit_products(request):
    if request.method == 'GET':
        # 상단 추천상품 1 - 최고우대금리가 가장 높은 상품
        options = DepositOptions.objects.order_by('-intr_rate2')[0]
        opt_serializer = DepositOptionsSerializer(options)
        product = options.product
        pro_serializer = DepositProductsSerializer(product)
        highest_intr_rate2 = {
            'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
            'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
            'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
            'intr_rate2':opt_serializer.data.get('intr_rate2'),
            'save_trm':opt_serializer.data.get('save_trm')
        }
        
        # 상단 추천상품 2 - 저축기간이 가장 짧은 상품 (개월)
        options = DepositOptions.objects.order_by('save_trm')[0]
        opt_serializer = DepositOptionsSerializer(options)
        product = options.product
        pro_serializer = DepositProductsSerializer(product)
        lowest_save_trm = {
            'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
            'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
            'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
            'intr_rate2':opt_serializer.data.get('intr_rate2'),
            'save_trm':opt_serializer.data.get('save_trm')
        }

        # 전체 상품 조회
        display_list = []
        for product in DepositProducts.objects.all():
            pro_serializer = DepositProductsSerializer(product)
            options = product.deposit_option.order_by('-intr_rate_type_nm','-intr_rate2')[0]
            opt_serializer = DepositOptionsSerializer(options)
            display = {
                'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
                'intr_rate2':opt_serializer.data.get('intr_rate2'),
                'save_trm':opt_serializer.data.get('save_trm')
            }
            display_list.append(display)
        data = {
            'highest_intr_rate2':highest_intr_rate2,
            'lowest_save_trm':lowest_save_trm,
            'display':display_list
        }
        return Response(data)


# 적금 조회
@api_view(['GET'])
def installment_products(request):
    if request.method == 'GET':
        # 상단 추천상품 1 - 최고우대금리가 가장 높은 상품
        options = InstallmentOptions.objects.order_by('-intr_rate2')[0]
        opt_serializer = InstallmentOptionsSerializer(options)
        product = options.product
        pro_serializer = InstallmentProductsSerializer(product)
        highest_intr_rate2 = {
            'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
            'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
            'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
            'intr_rate2':opt_serializer.data.get('intr_rate2'),
            'save_trm':opt_serializer.data.get('save_trm')
        }
        
        # 상단 추천상품 2 - 저축기간이 가장 짧은 상품 (개월)
        options = InstallmentOptions.objects.order_by('save_trm')[0]
        opt_serializer = InstallmentOptionsSerializer(options)
        product = options.product
        pro_serializer = InstallmentProductsSerializer(product)
        lowest_save_trm = {
            'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
            'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
            'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
            'intr_rate2':opt_serializer.data.get('intr_rate2'),
            'save_trm':opt_serializer.data.get('save_trm')
        }

        # 전체 상품 조회
        display_list = []
        for product in InstallmentProducts.objects.all():
            pro_serializer = InstallmentProductsSerializer(product)
            options = product.installment_option.order_by('-intr_rate_type_nm','-intr_rate2')[0]
            opt_serializer = InstallmentOptionsSerializer(options)
            display = {
                'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                'intr_rate_type_nm':opt_serializer.data.get('intr_rate_type_nm'),
                'intr_rate2':opt_serializer.data.get('intr_rate2'),
                'save_trm':opt_serializer.data.get('save_trm')
            }
            display_list.append(display)
        data = {
            'highest_intr_rate2':highest_intr_rate2,
            'lowest_save_trm':lowest_save_trm,
            'display':display_list
        }
        return Response(data)

# 연금 저축 조회
@api_view(['GET'])
def annuity_products(request):
    utc_now = timezone.now()
    kst = pytz.timezone('Asia/Seoul')
    now = utc_now.astimezone(kst).date()
    if request.method == 'GET':
        # 상단 추천상품 1 - 공시이율이 가장 높은 상품
        products = AnnuityProducts.objects.filter(Q(dcls_end_day__gt=now) | Q(dcls_end_day__isnull=True)).order_by('-dcls_rate')[0]
        pro_serializer = AnnuityProductsSerializer(products)
        options = products.annuity_option.order_by('paym_prd')[0]
        opt_serializer = AnnuityOptionsSerializer(options)
        highest_dcls_rate = {
            'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
            'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
            'dcls_rate':pro_serializer.data.get('dcls_rate'),
            'pnsn_entr_age':opt_serializer.data.get('pnsn_entr_age'),
            'pnsn_strt_age':opt_serializer.data.get('pnsn_strt_age'),
            'paym_prd':opt_serializer.data.get('paym_prd'),
            'mon_paym_atm':opt_serializer.data.get('mon_paym_atm'),
        }
        
        # 상단 추천상품 2 - 납입 기간이 가장 짧은 상품 (년)
        for option in AnnuityOptions.objects.order_by('paym_prd'):
            opt_serializer = AnnuityOptionsSerializer(option)
            product = option.product
            if product.dcls_end_day is None or product.dcls_end_day > now:
                pro_serializer = AnnuityProductsSerializer(product)
                lowest_paym_prd = {
                    'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                    'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                    'dcls_rate':pro_serializer.data.get('dcls_rate'),
                    'pnsn_entr_age':opt_serializer.data.get('pnsn_entr_age'),
                    'pnsn_strt_age':opt_serializer.data.get('pnsn_strt_age'),
                    'paym_prd':opt_serializer.data.get('paym_prd'),
                    'mon_paym_atm':opt_serializer.data.get('mon_paym_atm'),
                }
                break
            break

        # 상단 추천상품 3 - 월 납입 금액이 가장 적은 상품
        for option in AnnuityOptions.objects.order_by('mon_paym_atm'):
            opt_serializer = AnnuityOptionsSerializer(option)
            product = option.product
            if product.dcls_end_day is None or product.dcls_end_day > now:
                pro_serializer = AnnuityProductsSerializer(product)
                lowest_mon_paym_atm = {
                    'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                    'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                    'dcls_rate':pro_serializer.data.get('dcls_rate'),
                    'pnsn_entr_age':opt_serializer.data.get('pnsn_entr_age'),
                    'pnsn_strt_age':opt_serializer.data.get('pnsn_strt_age'),
                    'paym_prd':opt_serializer.data.get('paym_prd'),
                    'mon_paym_atm':opt_serializer.data.get('mon_paym_atm'),
                }
                break
            break

        # 전체 상품 조회
        display_list = []
        for product in AnnuityProducts.objects.order_by('-dcls_rate'):
            pro_serializer = AnnuityProductsSerializer(product)
            options = product.annuity_option.order_by('paym_prd')[0]
            opt_serializer = AnnuityOptionsSerializer(options)
            if product.dcls_end_day is None or product.dcls_end_day > now:
                end_day = True
            else:
                end_day = False
            display = {
                'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                'dcls_rate':pro_serializer.data.get('dcls_rate'),
                'pnsn_entr_age':opt_serializer.data.get('pnsn_entr_age'),
                'pnsn_strt_age':opt_serializer.data.get('pnsn_strt_age'),
                'paym_prd':opt_serializer.data.get('paym_prd'),
                'mon_paym_atm':opt_serializer.data.get('mon_paym_atm'),
                'dcls_end_day': end_day,
            }
            display_list.append(display)
        data = {
            'highest_dcls_rate':highest_dcls_rate,
            'lowest_paym_prd':lowest_paym_prd,
            'lowest_mon_paym_atm':lowest_mon_paym_atm,
            'display':display_list
        }
        return Response(data)


# 신용 대출 조회
@api_view(['GET'])
def creditLoan_products(request):
    utc_now = timezone.now()
    kst = pytz.timezone('Asia/Seoul')
    now = utc_now.astimezone(kst).date()
    if request.method == 'GET':
        # 상단 추천상품 1 - 대출금리가 가장 낮은 상품
        for option in creditLoanOptions.objects.filter(crdt_lend_rate_type='A').order_by('crdt_grad_avg'):
            opt_serializer = creditLoanOptionsSerializer(option)
            product = option.product
            if product.dcls_end_day is None or product.dcls_end_day > now:
                pro_serializer = creditLoanProductsSerializer(product)
                lowest_crdt_grad_avg = {
                    'kor_co_nm': pro_serializer.data.get('kor_co_nm'),
                    'fin_prdt_nm': pro_serializer.data.get('fin_prdt_nm'),
                    'crdt_prdt_type_nm': pro_serializer.data.get('crdt_prdt_type_nm'),
                    'crdt_lend_rate_type_nm': opt_serializer.data.get('crdt_lend_rate_type_nm'),
                    'crdt_grad_avg': opt_serializer.data.get('crdt_grad_avg'),
                }
                break
            break
        
        # 상단 추천상품 2 - 가감조정금리가 가장 높은 상품
        for option in creditLoanOptions.objects.filter(crdt_lend_rate_type='D').order_by('-crdt_grad_avg'):
            opt_serializer = creditLoanOptionsSerializer(option)
            product = option.product
            if product.dcls_end_day is None or product.dcls_end_day > now:
                pro_serializer = creditLoanProductsSerializer(product)
                highest_crdt_grad_avg = {
                    'kor_co_nm': pro_serializer.data.get('kor_co_nm'),
                    'fin_prdt_nm': pro_serializer.data.get('fin_prdt_nm'),
                    'crdt_prdt_type_nm': pro_serializer.data.get('crdt_prdt_type_nm'),
                    'crdt_lend_rate_type_nm': opt_serializer.data.get('crdt_lend_rate_type_nm'),
                    'crdt_grad_avg': opt_serializer.data.get('crdt_grad_avg'),
                }
                break
            break

        # 전체 상품 조회
        display_list = []
        for product in creditLoanProducts.objects.all():
            pro_serializer = creditLoanProductsSerializer(product)
            options = product.creditLoan_option.filter(crdt_lend_rate_type='A').order_by('crdt_grad_avg')[0]
            opt_serializer = creditLoanOptionsSerializer(options)
            if product.dcls_end_day is None or product.dcls_end_day > now:
                end_day = True
            else:
                end_day = False

            display = {
                'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                'crdt_prdt_type_nm':pro_serializer.data.get('crdt_prdt_type_nm'),
                'crdt_lend_rate_type_nm':opt_serializer.data.get('crdt_lend_rate_type_nm'),
                'crdt_grad_avg':opt_serializer.data.get('crdt_grad_avg'),
                'dcls_end_day':end_day,
            }
            display_list.append(display)
        data = {
            'lowest_crdt_grad_avg_A':lowest_crdt_grad_avg,
            'highest_crdt_grad_avg_D':highest_crdt_grad_avg,
            'display':display_list
        }
        return Response(data)










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


@api_view(['GET','POST'])
def nn(request):
    products = DepositProducts.objects.all()
    if request.method == 'GET':
        for product in DepositProducts.objects.all():
            pro_serializer = DepositProductsSerializer(product)
            options = product.deposit_option.order_by('-intr_rate_type_nm','-intr_rate2')[0]
            opt_serializer = DepositOptionsSerializer(options)
            data = {
                'product':pro_serializer.data,
                'option':opt_serializer.data
            }
            break
        return Response(data)
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)