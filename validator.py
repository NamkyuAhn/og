import re

REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
REGEX_PHONE_NUMBER = '(?P<area>\d{3})-(?P<num>\d{4}-\d{4})'
REGEX_DATE = r'\d{4}-\d{2}-\d{2}'

def email_validate(value):
    if not re.match(REGEX_EMAIL,value):
        return True

def phone_number_validate(value):
    if not re.match(REGEX_PHONE_NUMBER, value):
        return True

def gender_validate(value):
    if value == '남성' or value == '여성':
        return True

def date_validate(value):
    if not re.match(REGEX_DATE, value):
        return True
