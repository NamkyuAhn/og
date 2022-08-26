from datetime import date

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Q, Value, CharField, Func
from django.db.models.functions import Concat

from .models import Artist, ArtistEntry, Item, Exhibition, ExhibitionItem
from .forms import ArtistEntryForm, ItemEntryForm, ExhibitionEntryForm, ItemForExhibitionForm

from validator import phone_number_validate

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'

def main(request):
	return render(request, 'index.html', {})

def artist_entry(request):
	if request.user.is_authenticated:
		if ArtistEntry.objects.filter(user_id = request.user.id).exists():#중복 지원 X
				messages.info(request, "이미 등록된 작가거나 작가 등록 심사중 입니다.")
				return redirect('og:main')

		if request.method == 'POST':
			form = ArtistEntryForm(request.POST)

			if form.is_valid():
				if phone_number_validate(form.data['phone_number']):#전화번호 형식 검사
					messages.info(request, "전화번호 형식을 000-0000-0000 과 같이 입력하세요.")
					return redirect('og:artist_entry')

				artist_entry = ArtistEntry(
					name = form.data['username'],
					email = form.data['email'],
					phone_number = form.data['phone_number'],
					gender = form.data['gender'],
					birth_date = form.data['birth_date'],
					is_checked = False,
					is_approved = False,
					user_id = request.user.id
				)
				artist_entry.save()

				messages.info(request, "작가님의 정보가 등록되었습니다. 심사 후 작가에 등록해 드립니다.")
				return redirect('og:main')

			else :
				messages.warning(request, "작성 폼을 올바르게 입력 하였는지 다시 한번 확인해 주세요.")
				return redirect('og:artist_entry')

		else: #GET일때
			form = ArtistEntryForm()
			return render(request, 'artist_entry.html', {'form' : form})

	else: #로그인 안했을때
		messages.warning(request, "로그인이 필요한 서비스입니다.")
		return redirect('accounts:login')

def artist_menu(request):
	if request.user.is_authenticated:
		if Artist.objects.filter(user_id = request.user.id).exists():
			artist_info = Artist.objects.filter(user_id = request.user.id)
			artist_id = Artist.objects.get(user_id = request.user.id).id

			if Item.objects.filter(artist_id = artist_id).exists():
				items = Item.objects.all().annotate(
						int_price = Round(Avg('price')),
						)\
					.values('item_name', 'int_price', 'size')\
					.order_by('-created_at')
			else: 
				items = False
			
			if Exhibition.objects.filter(artist_id = artist_id).exists():
				exhibitions = Exhibition.objects.filter(artist_id = artist_id)
			else:
				exhibitions = False
			print(artist_info[0].phone_number)
			return render(request, 'artist_menu.html', {'artist_info' : artist_info, 'items' : items, 'exhibitions' : exhibitions, 'phone_number' : artist_info[0].phone_number})

		messages.info(request, "아직 작가에 등록하지 않으셨거나 작가 승인이 되지 않았습니다.")
		return redirect ('og:main')
	else:
		messages.warning(request, "로그인이 필요한 서비스입니다.")
		return redirect ('accounts:login')

def item_entry(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = ItemEntryForm(request.POST)
			if form.is_valid():
				artist_id = Artist.objects.get(user_id = request.user.id).id
				item = Item(
					item_name = form.data['item_name'],
					price = int(request.POST['price'].replace(",", "")),
					size = form.data['size'],
					artist_id = artist_id
				)
				item.save()
				messages.info(request, "작품 정보가 등록되었습니다.")
				return redirect('og:artist_menu')

			else :
				messages.warning(request, "작성 폼을 올바르게 입력 하였는지 다시 한번 확인해 주세요.")
				return redirect('og:item_entry')

		else: #GET일때
			form = ItemEntryForm()
			return render(request, 'item_entry.html', {'form' : form})

	else: #로그인 안했을때
		messages.warning(request, "로그인 창으로 이동합니다.")
		return redirect('accounts:login')

def exhibition_entry(request):
	if request.user.is_authenticated:

		if request.method == 'POST':
			artist_id = Artist.objects.get(user_id = request.user.id).id
			exhibition_form = ExhibitionEntryForm(request.POST)
			item_form = ItemForExhibitionForm(request.POST.getlist('item_name'), artist_id = artist_id)
			print(item_form.data)

			if exhibition_form.is_valid() and item_form.is_valid():
				artist_id = Artist.objects.get(user_id = request.user.id).id
				exhibition = Exhibition(
					exhibition_name = exhibition_form.data['exhibition_name'],
					starting_date = exhibition_form.data['starting_date'],
					ending_date = exhibition_form.data['ending_date'],
					artist_id = artist_id
				)
				exhibition.save()
				for item_id in item_form.data['item_name']:
					exhibition_item = ExhibitionItem(
						exhibition_id = exhibition.id,
						item_id = item_id
					)
					exhibition_item.save()
				messages.info(request, "전시 정보가 등록되었습니다.")
				return redirect('og:artist_menu')

			else :
				messages.warning(request, "작성 폼을 올바르게 입력 하였는지 다시 한번 확인해 주세요.")
				return redirect('og:exhibition_entry')

		else: #GET일때
			exhibition_form = ExhibitionEntryForm()
			artist_id = Artist.objects.get(user_id = request.user.id).id
			item_form = ItemForExhibitionForm(artist_id = artist_id)
			return render(request, 'exhibition_entry.html', {'exhibition_form' : exhibition_form, 'item_form' : item_form})

	else: #로그인 안했을때
		messages.warning(request, "로그인 창으로 이동합니다.")
		return redirect('accounts:login')

def artist_stat(request):
	if request.user.is_staff:
		artists = Artist.objects.all().prefetch_related('item_set')\
			.annotate(
				avg_price = Round(Avg('item__price')),
				total_item = Count('item', filter = Q(item__size__lte = 100)),
			)\
			.values('name', 'avg_price', 'total_item')\
			.order_by('created_at')
		return render(request, 'artist_stat.html', {'artists' : artists})

	else:
		messages.warning(request, "관리자 계정만 접근이 가능합니다.")
		return redirect('og:main')

def admin_menu(request):
	if request.user.is_staff:
		return render(request, 'admin_menu.html')

	else:
		messages.warning(request, "관리자 계정만 접근이 가능합니다.")
		return redirect('og:main')
		
def artist_list(request):
	artists = Artist.objects.all().order_by('-created_at')
	return render(request, 'artist_list.html', {'artists' : artists})

def item_list(request):
	items = Item.objects.all().select_related('artist')\
		.annotate(
			artist_name = Concat('artist__name', Value(''), output_field = CharField()),
			int_price = Round(Avg('price')),
		)\
		.values('item_name', 'int_price', 'size', 'artist_name')\
		.order_by('-created_at')
	return render(request, 'item_list.html', {'items' : items})