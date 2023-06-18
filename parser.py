import csv
from dataclasses import dataclass, field
from typing import List, Union


sample = [['2022-01-17','Branch Transaction SERVICE CHARGE CAPPED MONTHLY FEE$16.95 RECORD-KEEPING N/A','16.99',''],
          ['2022-01-17','Electronic Funds Transfer PREAUTHORIZED DEBIT BANK BANK MORTGAGE DEPT (PAY)', '100.00',''],
          ['2022-03-17','Internet Banking INTERNET BILL PAY 0000001 PANDA MOBILE','1000.00',''],
          ['2022-04-17','Point of Sale - Interac RETAIL PURCHASE 0000012 S-MART #0001','400.00',''],
          ['2022-04-17','Internet Banking E-TRANSFER 000000001234 JOHN SMITH','','250.00'],
          ['2022-04-17','Electronic Funds Transfer PAY PAYROLL PAYROLL','','6000.00'],
          ['2022-05-17','Point of Sale - Interac RETAIL PURCHASE D3ADB33F0000 Subshop 00001','16.00','']]

@dataclass
class Summary:
    pass
    

@dataclass
class Transaction:
    '''
    Transactions can be a purchase, deposit, transfer etc.
    Generally there is only a transaction ID if it is a
    purchase, e-transfer or bill payment
    '''
    tr_label: str # method or action
    tr_type: str # what was the purpose
    tr_id: str  # transaction ID (contingent)
    tr_agent: str # party to the transaction (contingent)


@dataclass
class Line:
    '''
    This is an entry in the transaction record
    and is either a debit or a credit
    '''
    tr_date: str
    tr_data: Transaction
    tr_debit: float
    tr_credit: float
    tr_type: str

def contains_numbers(s: str) -> bool:
    '''
    helper function to parse_transaction_type
    to parse out the odd alpha numeric transaction
    number
    '''
    for l in s:
        if l.isnumeric():
            return True
    return False

def parse_transaction_type(t: str) -> tuple:
    l = t.split()
    t_n = 0
    cat = {}
    tr_description = None
    tr_type = None
    tr_number = ''
    tr_agent = ''

    # find transaction tag
    words = []
    for w in l:
        if w.istitle() or w.islower() or w == '-':
            words.append(w)
        if w.isupper():
            break
    tr_description = ' '.join([w for w in words if not w.isupper()])

    # find transaction type
    u_words = []
    for w in l:
        if w.isupper():
            if contains_numbers(w):
                pass
            else:
                u_words.append(w)
        if w.isnumeric():
            break
    tr_type = ' '.join([w for w in u_words if not w.isnumeric()])
            
    # find a transaction number
    for k, w in enumerate(l):
        if w.isnumeric() or contains_numbers(w):
            t_n = k
            tr_number = l[k]
            break
            
    # find the name of the business, recipient or depositor
    if t_n and len(l) > t_n + 1:
        tr_agent = ' '.join(l[t_n +1:])
            
    return tr_description, tr_type, tr_number, tr_agent
    
    
def parse_file(f_path: list) -> list:
    f = []
    for l in f_path:
        d_or_c = 'Credit'
        #tr = Transaction(parse_transaction_type(l[1]))
        if l[2]:
            d_or_c = 'Debit'
        ptt = parse_transaction_type(l[1])
        print(ptt)
        action = Transaction(ptt[0],ptt[1],ptt[2],ptt[3])
        f.append(Line(l[0], action, l[2], l[3], d_or_c))
    return f

# Testing Zone


test = parse_file(sample)

for l in test:
    if l.tr_type == 'Debit' and l.tr_data.tr_agent:
        print(l.tr_data.tr_agent, l.tr_data.)

    
