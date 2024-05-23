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
import random
import pandas as pd
import joblib
import os
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from sklearn.model_selection import train_test_split

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
            'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, '/assets/icons/banks/default-logo.svg'),
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
            'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, '/assets/icons/banks/default-logo.svg'),
        }
        recommend.append(lowest_save_trm)

        # 상단 추천상품 3 - 가장 많은 사람들이 찾은 상품
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)
        pro_list = []
        for product in user_serializer.data:
            pro_list.extend(product.get('product'))
        number = max(pro_list)

        product = DepositProducts.objects.get(pk=number)
        pro_serializer = DepositProductsSerializer(product)
        options = product.deposit_option.order_by('-intr_rate_type_nm','-intr_rate2')[0]
        opt_serializer = DepositOptionsSerializer(options)

        id = pro_serializer.data.get('id')
        kor_co_nm = pro_serializer.data.get('kor_co_nm')
        fin_prdt_nm = pro_serializer.data.get('fin_prdt_nm')
        pro_type = pro_serializer.data.get('product_type')
        intr_rate2 = opt_serializer.data.get('intr_rate2')

        many_people_like = {
            'id':id,
            'kor_co_nm':kor_co_nm,
            'fin_prdt_nm':fin_prdt_nm,
            'text': "가장 많은 사람들이 찾았어요! 🥳",
            'tags':[pro_type, str(intr_rate2)+"%"],
            'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, '/assets/icons/banks/default-logo.svg'),
        }
        recommend.append(many_people_like)

        # 전체 상품 조회
        display_list = []
        for product in DepositProducts.objects.all():
            pro_serializer = DepositProductsSerializer(product)
            options = product.deposit_option.order_by('-intr_rate_type_nm','-intr_rate2')[0]
            opt_serializer = DepositOptionsSerializer(options)
            kor_co_nm = pro_serializer.data.get('kor_co_nm')
            display = {
                'id':pro_serializer.data.get('id'),
                'kor_co_nm':kor_co_nm,
                'fin_prdt_nm':pro_serializer.data.get('fin_prdt_nm'),
                'intr_rate2':opt_serializer.data.get('intr_rate2'),
                'save_trm':opt_serializer.data.get('save_trm'),
                'product_type':pro_serializer.data.get('product_type'),
                'imgUrl': BANK_IMAGE_URL_DICT.get(kor_co_nm, '/assets/icons/banks/default-logo.svg'),
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
        kor_co_nm = pro_serializer.data.get('kor_co_nm')
        pro = pro_serializer.data
        pro['imgUrl'] = BANK_IMAGE_URL_DICT.get(kor_co_nm, '/assets/icons/banks/default-logo.svg')
        comment_list = []
        for comment in products.product_set.all():
            com_serializer = DepositCommentSerializer(comment)
            user_serializer = UserSerializer(comment.user)
            comment_data = {
                "nickname": user_serializer.data.get("nickname"),
                "id": com_serializer.data.get('id'),
                "content": com_serializer.data.get("content"),
                "created_at": com_serializer.data.get('created_at'),
            }
            comment_list.append(comment_data)
        data={
            'product':pro,
            'options':opt_serializer.data,
            'comment':comment_list
        }
        return Response(data, status=status.HTTP_200_OK)
    # 상품 댓글 달기
    elif request.method == 'POST':
        serializer = DepositCommentSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user, product = products)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

####################### 예금 적금 상품 찜하기 ##############################
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def like_deposit(request, product_pk):
    if request.user.is_authenticated:
        product = get_object_or_404(DepositProducts, pk=product_pk)
        if request.user in product.like_product.all():
            product.like_product.remove(request.user)
        else:
            product.like_product.add(request.user)
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
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        # user_serializer = UserSerializer(user, data=request.data, partial=True)
        # if user_serializer.is_valid(raise_exception=True):
        #         user_serializer.save()
        user_serializer = UserSerializer(user)
        df_data = {
            'birth': [],
            'gender': [],
            'crdt_grad': [],
            'salary': [],
            'm_consumption':[],
            'asset':[],
            'real_estate':[],
            'invest_tendency':[],
            'pro_cnt':[],   # 보유하고 있는 예적금 상품 수 1~5 (5 이상 입력하면 5로 변경)
            
            'join_deny': [],
            'join_member': [],
            'join_way': [],   # 스마트폰, 영업점, 인터넷, 전화(텔레뱅킹), 기타, 모집인
            'join_way_cnt': [],
            'type': [],       # 예금, 적금
            'intr_rate_type_nm': [],  # 단리, 복리
            'intr_rate': [],
            'intr_rate2': [],
            'save_trm': [],
            'rsrv_type': []
        }
        birth = user_serializer.data.get('birth')
        gender = request.data.get('gender')
        crdt_grad = request.data.get('crdt_grad')
        salary = request.data.get('salary')
        m_consumption = request.data.get('m_consumption')
        asset = request.data.get('asset')
        real_estate = request.data.get('real_estate')
        invest_tendency = request.data.get('invest_tendency')
        pro_cnt = request.data.get('pro_cnt')
        join_deny = random.choice([1, 3])
        join_member = "제한없음"
        join_way_cnt = len(request.data.get('join_way'))
        intr_rate = request.data.get('intr_rate')
        intr_rate2 = request.data.get('intr_rate')
        save_trm = request.data.get('save_trm')
        for join_way in request.data.get('join_way'):
            for type in request.data.get('type'):
                for intr_rate_type_nm in request.data.get('intr_rate_type_nm'):
                    df_data['birth'].append(birth)
                    df_data['gender'].append(gender)
                    df_data['crdt_grad'].append(crdt_grad)
                    df_data['salary'].append(salary)
                    df_data['m_consumption'].append(m_consumption)
                    df_data['asset'].append(asset)
                    df_data['real_estate'].append(real_estate)
                    df_data['invest_tendency'].append(invest_tendency)
                    df_data['pro_cnt'].append(pro_cnt)
                    df_data['join_deny'].append(join_deny)

                    df_data['join_member'].append(join_member)
                    df_data['join_way_cnt'].append(join_way_cnt)
                    df_data['intr_rate'].append(intr_rate)
                    df_data['intr_rate2'].append(intr_rate2)
                    df_data['save_trm'].append(save_trm)
                    df_data['join_way'].append(join_way)
                    df_data['type'].append(type)
                    df_data['intr_rate_type_nm'].append(intr_rate_type_nm)
                    if type == "예금":
                        df_data['rsrv_type'].append(random.choice(["N", "F", "S"]))
                    else:
                        df_data['rsrv_type'].append(random.choice(["F", "S"]))
        df = pd.DataFrame(df_data)
        print(df_data)
        # 나이
        df['age'] = df['birth'].apply(lambda x: datetime.now().year-int(x.split('-')[0])+1)
        # join_way의 갯수가 많은 순대로 가중치
        df['hot_join'] = df['join_way'].apply(lambda x: 7 if x == "스마트폰"
                                        else 6 if x == "영업점"
                                        else 5 if x =="인터넷"
                                        else 4 if x == "전화(텔레뱅킹)"
                                        else 3 if x == "기타"
                                        else 2 if x == "모집인"
                                        else 1)
        # 평균
        pro_df = df.groupby('birth')[['crdt_grad','salary','m_consumption','asset','intr_rate','intr_rate2','save_trm']].mean().reset_index()
        pro_df.rename(columns=lambda x: f"{x}_avg" if x != "birth" else x, inplace=True)
        df = df.merge(pro_df)
        # 소비 상황
        df.loc[df['salary'] < df['m_consumption']*12, "consumption"] = "과소비"
        df.loc[df['salary'] == df['m_consumption']*12, "consumption"] = "위험"
        df.loc[df['salary'] > df['m_consumption']*12, "consumption"] = "적정"


        ### 모델링
        df['birth'] = df['birth'].astype('str')
        df['gender'] = df['gender'].astype('category')
        df['real_estate'] = df['real_estate'].astype('category')
        df['invest_tendency'] = df['invest_tendency'].astype('category')

        # 범주형 변수와 수치형 변수를 분리
        cat_df = df.select_dtypes(include=['object','category']).columns.to_list()
        num_df = df.select_dtypes(exclude=['object','category']).columns.to_list()
        # 범주형 변수에 One-Hot-Encoding 후 수치형 변수와 병합
        if len(cat_df) > 0:
            df = pd.concat([df[num_df], pd.get_dummies(df[cat_df])], axis=1)
        else:
            df = df[num_df]

        model = joblib.load('recommend_model.pkl')
        scaler = joblib.load('scaler.pkl')

        scaler = StandardScaler()
        df = scaler.transform(df)
        predictions = model.predict(df)
        print(predictions)