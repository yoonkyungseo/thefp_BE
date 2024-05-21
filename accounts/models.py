from django.db import models
from django.contrib.auth.models import AbstractUser
from savedata.models import DepositProducts, AnnuityProducts, creditLoanProducts

# Create your models here.
class User(AbstractUser):
    birth = models.CharField(max_length=100)                    # 생일
    GENDER = (
        (0, 'Man'),
        (1, 'Woman')
    )
    gender = models.IntegerField(choices=GENDER, blank=True, null=True) # 성별  
    # CharField(max_length=1, choices=GENDER)
    crdt_grad = models.IntegerField(blank=True, null=True)           # 신용등급
    salary = models.IntegerField(blank=True, null=True)              # 연봉 (만원)
    m_consumption = models.IntegerField(blank=True, null=True)       # 평균 월 소비 (만원)
    product = models.ManyToManyField(DepositProducts)   # 가입한 예금 상품
    annuity = models.ManyToManyField(AnnuityProducts)   # 가입한 연금저축 상품
    creditloan = models.ManyToManyField(creditLoanProducts)   # 가입한 신용대출 상품


class Deposit_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_set')
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='product_set')
    content = models.TextField()