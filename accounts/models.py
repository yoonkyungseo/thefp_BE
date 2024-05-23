from django.db import models
from django.contrib.auth.models import AbstractUser
from savedata.models import DepositProducts, AnnuityProducts, creditLoanProducts
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

username_validator = UnicodeUsernameValidator()
# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    birth = models.DateField(max_length=100)                    # 생일
    GENDER = (
        (0, 'Man'),
        (1, 'Woman')
    )
    gender = models.IntegerField(choices=GENDER, blank=True, null=True) # 성별  
    # CharField(max_length=1, choices=GENDER)
    crdt_grad = models.IntegerField(blank=True, null=True)           # 신용등급
    salary = models.IntegerField(blank=True, null=True)              # 연봉 (만원)
    m_consumption = models.IntegerField(blank=True, null=True)       # 월 평균 소비 (만원)
    asset = models.IntegerField(blank=True, null=True)               # 순자산 (만원)
    real_estate = models.IntegerField(blank=True, null=True)              # 부동산 보유 여부 (0: 없음, 1: 있음)
    invest_tendency = models.IntegerField(blank=True, null=True)          # 투자성향 (1: 보수적, 5: 공격적)

    product = models.ManyToManyField(DepositProducts, related_name='like_product')   # 찜한 예금 상품
    annuity = models.ManyToManyField(AnnuityProducts, related_name='like_annuity')   # 찜한 연금저축 상품
    creditloan = models.ManyToManyField(creditLoanProducts, related_name='like_creditloan')   # 찜한 신용대출 상품


class Deposit_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_set')
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='product_set')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)