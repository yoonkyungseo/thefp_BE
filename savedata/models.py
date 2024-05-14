from django.db import models

# 예금 상품
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(default="")   # 금융상품코드
    kor_co_nm = models.TextField(default="")     # 금융회사명
    fin_prdt_nm = models.TextField(default="")   # 금융상품명
    etc_note = models.TextField(default="")      # 금융상품설명
    join_deny = models.IntegerField(default=-1)  # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField(default="")   # 가입대상
    join_way = models.TextField(default="")      # 가입방법
    spcl_cnd = models.TextField(default="")      # 우대조건

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='deposit_option') 
    fin_prdt_cd = models.TextField(default="")                        # 금융상품코드
    intr_rate_type_nm = models.CharField(max_length=100,default="")   # 저축금리 유형명
    intr_rate = models.FloatField(default=0, null=True)               # 저축금리
    intr_rate2 = models.FloatField(default=0)                         # 최고우대금리
    save_trm = models.IntegerField(default=0)                         # 저축기간(단위:개월)


# 적금 상품
class InstallmentProduct(models.Model):
    fin_prdt_cd = models.TextField(default="", blank=False, null=False)   # 금융상품코드
    kor_co_nm = models.TextField(default="")     # 금융회사명
    fin_prdt_nm = models.TextField(default="")   # 금융상품명
    etc_note = models.TextField(default="")      # 기타 유의사항
    join_deny = models.IntegerField(default=-1)  # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField(default="")   # 가입대상
    join_way = models.TextField(default="")      # 가입방법
    spcl_cnd = models.TextField(default="")      # 우대조건

class InstallmentOption(models.Model):
    product = models.ForeignKey(InstallmentProduct, on_delete=models.CASCADE, related_name='installment_option') 
    fin_prdt_cd = models.TextField(default="")                        # 금융상품코드
    intr_rate_type_nm = models.CharField(max_length=100,default="")   # 저축금리 유형명
    intr_rate = models.FloatField(default=0, null=True)               # 저축금리
    intr_rate2 = models.FloatField(default=0)                         # 최고우대금리
    save_trm = models.IntegerField(default=0)                         # 저축기간(단위:개월)
    rsrv_type = models.TextField(default="")                          # 적립유형명
    rsrv_type = models.TextField(default="")                          # 적립유형
    

# 연금저축 상품
class AnnuityProduct(models.Model):
    fin_prdt_cd = models.TextField(default="")      # 금융상품코드
    kor_co_nm = models.TextField(default="")        # 금융회사명
    fin_prdt_nm = models.TextField(default="")      # 금융상품명
    etc = models.TextField(default="")              # 기타사항
    join_way = models.TextField(default="")         # 가입방법
    pnsn_kind_nm = models.TextField(default="")     # 연금종류명
    mntn_cnt = models.IntegerField(default=0)       # 유지건수(건) 또는 설정액(원)
    prdt_type_nm = models.TextField(default="")     # 상품유형명
    dcls_rate = models.FloatField(default=0)        # 공시이율 [소수점 2자리]
    guar_rate = models.FloatField(default=0)        # 최저 보증이율
    btrm_prft_rate_1 = models.FloatField(default=0) # 전년도 수익률
    btrm_prft_rate_2 = models.FloatField(default=0) # 전전년도 수익률
    sale_co = models.TextField(default="")          # 판매사
    dcls_strt_day = models.DateTimeField()          # 공시 시작일
    dcls_end_day = models.DateTimeField()           # 공시 종료일

class AnnuityOption(models.Model):
    product = models.ForeignKey(AnnuityProduct, on_delete=models.CASCADE, related_name='annuity_option') 
    fin_prdt_cd = models.TextField(default="")                        # 금융상품코드
    pnsn_recp_trm = models.TextField(default="")                      # ????? A: 10년확정, B: 20년확정,,,,,
    pnsn_entr_age = models.IntegerField(default=0)                    # 가입가능 최소나이
    mon_paym_atm = models.IntegerField(default=0)                     # 월 납입 금액 (만원)
    paym_prd = models.IntegerField(default=0)                         # 납입 기간 (년)
    pnsn_strt_age = models.IntegerField(default=0)                    # 수령 가능 최소 나이
    pnsn_recp_amt =  models.IntegerField(default=0)                   # ???? 아마도 가격 혹은 수량


# 개인 신용 대출
class creditLoanProduct(models.Model):
    fin_prdt_cd = models.TextField(default="")       # 금융상품코드
    kor_co_nm = models.TextField(default="")         # 금융회사명
    fin_prdt_nm = models.TextField(default="")       # 금융상품명
    join_way = models.TextField(default="")          # 가입방법
    crdt_prdt_type = models.IntegerField(default=0)  # 대출 종류 코드
    crdt_prdt_type_nm = models.TextField(default="") # 대출 종류명
    cb_name = models.TextField(default="")           # CB회사명 (신용조회회사)
    dcls_strt_day = models.DateTimeField()           # 공시 시작일
    dcls_end_day = models.DateTimeField()            # 공시 종료일

class creditLoanOption(models.Model):
    product = models.ForeignKey(creditLoanProduct, on_delete=models.CASCADE, related_name='annuity_option') 
    crdt_lend_rate_type = models.TextField(default="")         # 금리구분코드
    crdt_lend_rate_type_nm = models.TextField(default="")      # 금리구분
    crdt_grad_1 = models.FloatField(default=0)                 # 900점 초과
    crdt_grad_4 = models.FloatField(default=0)                 # 801~900점
    crdt_grad_5 = models.FloatField(default=0)                 # 701~800점
    crdt_grad_6 = models.FloatField(default=0)                 # 601~700점
    crdt_grad_10 = models.FloatField(default=0)                # 501~600점
    crdt_grad_11 = models.FloatField(default=0)                # 401~500점
    crdt_grad_12 = models.FloatField(default=0)                # 301~400점
    crdt_grad_13 = models.FloatField(default=0)                # 300점 이하
    crdt_grad_avg = models.FloatField(default=0)               # 평균 금리

