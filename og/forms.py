from django import forms
from django.core.validators import RegexValidator
from .models import ArtistEntry
from validator import phone_number_validate, gender_validate, date_validate

class ArtistEntryForm(forms.Form):

    CHOICES = [('남성','남성'), ('여성', '여성')]

    username = forms.CharField(label = '이름', max_length = 16, required = True)
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label = '성별', required = True)
    birth_date = forms.DateField(label = '생년월일', required = True)
    email = forms.EmailField(label = '이메일', required = True)
    phone_number = forms.CharField(label = '전화번호', max_length=13, required = True)