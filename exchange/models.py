from django.db import models

# 환율 정보
class ExchangeRate(models.Model):
    cur_unit = models.TextField()                     # 통화코드
    cur_nm = models.TextField()                       # 통화명
    ttb = models.TextField()                       # 전신환(송금) 받으실때
    tts = models.TextField()                     # 전신환(송금) 보내실때
    deal_bas_r = models.TextField()      # 매매 기준율
    kftc_deal_bas_r = models.TextField()           # 서울외국환중개 매매기준율