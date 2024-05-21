def save_DepositProducts(data):
    for key in ['etc_note', 'join_member','join_way']:
        if data[key] == None:
            data[key] = "정보 없음"
    if data['join_deny'] == None:
        data['join_deny'] = 4
    if data['spcl_cnd'] == None:
        data['spcl_cnd'] = "우대조건 없음"

def save_AnnuityProduct(data):
    if data['etc'] == None:
        data['etc'] = "기타사항 없음"
    for key in ['join_way', 'pnsn_kind_nm','sale_co','guar_rate']:
        if data[key] == None:
            data[key] = "정보 없음"
    for key in ['dcls_strt_day','dcls_end_day']:
        if data[key] != None:
            data[key] = data[key][:4]+'-'+data[key][4:6]+'-'+data[key][6:]
    for key in ['mntn_cnt','dcls_rate','btrm_prft_rate_1','btrm_prft_rate_2']:
        if data[key] == None:
            data[key] = 0

def save_LoanProduct(data):
    for key in ['join_way', 'cb_name']:
        if data[key] == None:
            data[key] = "정보 없음"
    for key in ['dcls_strt_day','dcls_end_day']:
        if data[key] == None:
            data[key] = ""
        else:
            data[key] = data[key][:4]+'-'+data[key][4:6]+'-'+data[key][6:]
def save_LoanOptions(data):
    for key in ['crdt_grad_1','crdt_grad_4','crdt_grad_5','crdt_grad_6','crdt_grad_10','crdt_grad_11','crdt_grad_12','crdt_grad_13']:
        if data[key] == None:
            data[key] = 0