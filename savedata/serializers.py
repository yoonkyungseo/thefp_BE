from rest_framework import serializers
from .models import DepositOptions, DepositProducts
from .models import InstallmentOption, InstallmentProduct
from .models import AnnuityOption, AnnuityProduct
from .models import creditLoanOption, creditLoanProduct

# 예금
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ['product',]

# 적금
class InstallmentProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentProduct
        fields = '__all__'

class InstallmentOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentOption
        fields = '__all__'
        read_only_fields = ['product',]

# 연금저축
class AnnuityProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnuityProduct
        fields = '__all__'

class AnnuityOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnuityOption
        fields = '__all__'
        read_only_fields = ['product',]


# 개인 신용 대출
class creditLoanProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = creditLoanProduct
        fields = '__all__'

class creditLoanOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = creditLoanOption
        fields = '__all__'
        read_only_fields = ['product',]