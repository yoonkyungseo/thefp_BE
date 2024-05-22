from rest_framework import serializers
from .models import DepositOptions, DepositProducts
from .models import AnnuityOptions, AnnuityProducts
from .models import creditLoanOptions, creditLoanProducts

# 예금, 적금
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'
        read_only_fields = ['like',]

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ['product',]


# 연금저축
class AnnuityProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnuityProducts
        fields = '__all__'
        read_only_fields = ['like',]

class AnnuityOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnuityOptions
        fields = '__all__'
        read_only_fields = ['product',]


# 개인 신용 대출
class creditLoanProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = creditLoanProducts
        fields = '__all__'
        read_only_fields = ['like',]

class creditLoanOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = creditLoanOptions
        fields = '__all__'
        read_only_fields = ['product',]