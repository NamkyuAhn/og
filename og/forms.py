from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Item, Exhibition, Artist
from django.db.models.functions import Concat
from django.db.models           import Value, CharField

class ArtistEntryForm(forms.Form):
    CHOICES = [('남성','남성'), ('여성', '여성')]

    username = forms.CharField(label = '이름(16자 이하)', max_length = 16, required = True)
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label = '성별', required = True)
    birth_date = forms.DateField(label = '생년월일', required = True, help_text="YYYY-MM-DD 형식으로 입력")
    email = forms.EmailField(label = '이메일', required = True)
    phone_number = forms.CharField(label = '전화번호(하이픈 포함)', max_length=13, required = True)

class ItemEntryForm(forms.Form):
    item_name = forms.CharField(label = '제목 (64자 이하)', max_length=64)
    size = forms.IntegerField(label = '호수 (1~500 사이)', validators=[MinValueValidator(1), MaxValueValidator(500)])

class ExhibitionEntryForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ('exhibition_name', 'starting_date', 'ending_date')
        labels = {
            "exhibition_name": "제목(64자 이하)",
            "starting_date": "시작 날짜",
            "ending_date" : "종료 날짜"
        }

class ItemForExhibitionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.artist_id = kwargs.pop('artist_id')
        super(ItemForExhibitionForm, self).__init__(*args, **kwargs)
        queryset = Item.objects.filter(artist_id = self.artist_id).values_list('item_name')
        self.fields['item_name'] = forms.ModelChoiceField(queryset=queryset, widget=forms.CheckboxSelectMultiple(), label = '작품 이름')
        







