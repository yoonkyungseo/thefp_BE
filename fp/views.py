from savedata.serializers import DepositOptionsSerializer, DepositProductsSerializer
from savedata.serializers import AnnuityOptionsSerializer, AnnuityProductsSerializer
from savedata.serializers import creditLoanOptionsSerializer, creditLoanProductsSerializer
from savedata.models import DepositOptions, DepositProducts
from savedata.models import AnnuityOptions, AnnuityProducts
from accounts.models import Deposit_Comment
from accounts.models import User
from accounts.serializers import DepositCommentSerializer, UserSerializer
from savedata.models import creditLoanOptions, creditLoanProducts
from .bank_img import BANK_IMAGE_URL_DICT
from rest_framework.authentication import TokenAuthentication

from django.db.models import Q
from django.utils import timezone
import pytz
from rest_framework.decorators import api_view, authentication_classes
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
import requests

##################### 상품 조회 #######################
# 예금, 적금 조회
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def deposit_products(request):
    if request.method == 'GET':
        recommend = []
        # 상단 추천상품 1 - 최고우대금리가 가장 높은 상품
        options = DepositOptions.objects.order_by('-intr_rate2')[0]
        opt_serializer = DepositOptionsSerializer(options)
        product = options.product
        pro_serializer = DepositProductsSerializer(product)

        id = pro_serializer.data.get('id')
        kor_co_nm = pro_serializer.data.get('kor_co_nm')
        fin_prdt_nm = pro_serializer.data.get('fin_prdt_nm')
        pro_type = pro_serializer.data.get('product_type')
        intr_rate2 = opt_serializer.data.get('intr_rate2')
        highest_intr_rate2 = {
            'id':id,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'text': '가장 높은 최고우대금리를 가진 상품이에요📈',
            'tags':[pro_type, str(intr_rate2)+"%"],
            'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, ""),
        }
        recommend.append(highest_intr_rate2)
        
        # 상단 추천상품 2 - 저축기간이 가장 짧은 상품 (개월)
        options = DepositOptions.objects.order_by('save_trm')[0]
        opt_serializer = DepositOptionsSerializer(options)
        product = options.product
        pro_serializer = DepositProductsSerializer(product)

        id = pro_serializer.data.get('id')
        kor_co_nm = pro_serializer.data.get('kor_co_nm')
        fin_prdt_nm = pro_serializer.data.get('fin_prdt_nm')
        pro_type = pro_serializer.data.get('product_type')
        save_trm = opt_serializer.data.get('save_trm')

        lowest_save_trm = {
            'id':id,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'text': '저축기간이 가장 짧아요! 🏃',
            'tags':[pro_type, str(save_trm)+"개월"],
            'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, ""),
        }
        recommend.append(lowest_save_trm)

        # 전체 상품 조회
        display_list = []
        for product in DepositProducts.objects.all():
            pro_serializer = DepositProductsSerializer(product)
            options = product.deposit_option.order_by('-intr_rate_type_nm','-intr_rate2')[0]
            opt_serializer = DepositOptionsSerializer(options)
            display = {
                'id':pro_serializer.data.get('id'),
                'kor_co_nm':pro_serializer.data.get('kor_co_nm'),
                'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                'intr_rate2':opt_serializer.data.get('intr_rate2'),
                'save_trm':opt_serializer.data.get('save_trm'),
                'product_type':pro_serializer.data.get('product_type'),
                'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, ""),
            }
            display_list.append(display)
        data = {
            'recommend':recommend,
            'display':display_list
        }
        return Response(data, status=status.HTTP_200_OK)

# 연금 저축 조회
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def annuity_products(request):
    utc_now = timezone.now()
    kst = pytz.timezone('Asia/Seoul')
    now = utc_now.astimezone(kst).date()
    if request.method == 'GET':
        recommend = []
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
            'text': '공시이율이 가장 높은 상품',
            'tags':[],
            'imgUrl' :"",
        }
        recommend.append(highest_dcls_rate)
        
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
                    'text': '납입 기간이 가장 짧은 상품',
                    'tags':[],
                    'imgUrl' :"",
                }
                break
            break
        recommend.append(lowest_paym_prd)
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
                    'text': '월 납입 금액이 가장 적은 상품',
                    'tags':[],
                    'imgUrl' :"",
                }
                break
            break
        recommend.append(lowest_mon_paym_atm)
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
            'recommend':recommend,
            'display':display_list
        }
        return Response(data)


# 신용 대출 조회
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def creditLoan_products(request):
    utc_now = timezone.now()
    kst = pytz.timezone('Asia/Seoul')
    now = utc_now.astimezone(kst).date()
    if request.method == 'GET':
        recommend = []
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
                    'text': '대출금리가 가장 낮은 상품',
                    'tags':[],
                    'imgUrl' :"",
                }
                break
            break
        recommend.append(lowest_crdt_grad_avg)
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
                    'text': '가감조정금리가 가장 높은 상품',
                    'tags':[],
                    'imgUrl' :"",
                }
                break
            break
        recommend.append(highest_crdt_grad_avg)
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
            'recommend':recommend,
            'display':display_list
        }
        return Response(data)


########################## 상세 조회 ##############################
# 예금 적금 상품 상세조회
@authentication_classes([TokenAuthentication])
@api_view(['GET','POST'])
def deposit_product_options(request, pk):
    # 상품 상세조회
    products = DepositProducts.objects.get(pk=pk)
    if request.method == 'GET':
        options = products.deposit_option.all()
        opt_serializer = DepositOptionsSerializer(options, many=True)
        pro_serializer = DepositProductsSerializer(products)
        comment = products.product_set.all()
        com_serializer = DepositCommentSerializer(comment, many=True)
        data={
            'product':pro_serializer.data,
            'options':opt_serializer.data,
            'comment':com_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    # 상품 댓글 달기
    elif request.method == 'POST':
        serializer = DepositCommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user, product = products)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 예금 적금 상품 찜하기
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def like_deposit(request, product_pk):
    if request.user.is_authenticated:
        product = get_object_or_404(DepositProducts, pk=product_pk)
        if product.like_user.filter(pk=product_pk).exists():
            product.like_user.remove(request.user)
        else:
            product.like_user.add(request.user)
        return Response(status.HTTP_200_OK)


# 연금 저축 상세조회
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def annuity_product_options(request, pk):
    if request.method == 'GET':
        products = AnnuityProducts.objects.get(pk=pk)
        options = products.annuity_option.all()
        opt_serializer = AnnuityOptionsSerializer(options, many=True)
        pro_serializer = AnnuityProductsSerializer(products)
        data={
            'product':pro_serializer.data,
            'options':opt_serializer.data,
        }
        return Response(data)

# 신용대출 상세조회
@authentication_classes([TokenAuthentication])
@api_view(['GET'])
def creditLoan_product_options(request, pk):
    if request.method == 'GET':
        products = creditLoanProducts.objects.get(pk=pk)
        options = products.creditLoan_option.all()
        opt_serializer = creditLoanOptionsSerializer(options, many=True)
        pro_serializer = creditLoanProductsSerializer(products)
        data={
            'product':pro_serializer.data,
            'options':opt_serializer.data,
        }
        return Response(data)


######################### 추천 상품 ################################
@authentication_classes([TokenAuthentication])
@api_view(['POST'])
def recommend_product(request):
    user = User.objects.get(user = request.data.user)
    user_serializer = UserSerializer(user, data=request.data, partial=True)
    if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()