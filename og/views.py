from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Count, Q, Value, CharField, Func
from django.db.models.functions import Concat

from .models import Artist, ArtistEntry, Item, Exhibition, ExhibitionItem
from .forms import ArtistEntryForm, ItemEntryForm, ExhibitionEntryForm

from validator import phone_number_validate

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 0)'

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

def main(request):
	return render(request, 'index.html', {})

def artist_entry(request):
	if request.user.is_authenticated:

		if Artist.objects.filter(user_id = request.user.id).exists() or ArtistEntry.objects.filter(user_id = request.user.id, is_checked = False):
				messages.info(request, "이미 등록된 작가거나 심사중인 작가입니다.")
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
			return render(request, 'artist/artist_entry.html', {'form' : form})

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
			return render(request, 'artist/artist_menu.html', {'artist_info' : artist_info, 'items' : items, 'exhibitions' : exhibitions, 'phone_number' : artist_info[0].phone_number})

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
			return render(request, 'artist/item_entry.html', {'form' : form})

	else: #로그인 안했을때
		messages.warning(request, "로그인 창으로 이동합니다.")
		return redirect('accounts:login')

def exhibition_entry(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			artist_id = Artist.objects.get(user_id = request.user.id).id
			exhibition_form = ExhibitionEntryForm(request.POST)
			selected = request.POST.getlist('answers')

			if exhibition_form.is_valid():
				artist_id = Artist.objects.get(user_id = request.user.id).id
				exhibition = Exhibition(
					exhibition_name = exhibition_form.data['exhibition_name'],
					starting_date = exhibition_form.data['starting_date'],
					ending_date = exhibition_form.data['ending_date'],
					artist_id = artist_id
				)
				exhibition.save()

				for item_id in selected:
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
			items = Item.objects.filter(artist_id = artist_id)\
				.annotate(
				int_price = Round(Avg('price')),
			)
			return render(request, 'artist/exhibition_entry.html', {'exhibition_form' : exhibition_form, 'items' : items})

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
		return render(request, 'admin/artist_stat.html', {'artists' : artists})

	else:
		messages.warning(request, "관리자 계정만 접근이 가능합니다.")
		return redirect('og:main')

def admin_menu(request):
	if request.user.is_staff:
		if request.method == 'POST':
			approved_list = request.POST.getlist('approve')
			rejected_list = request.POST.getlist('reject')

			for artist_entry_id in approved_list:#승인 작가 처리
				if artist_entry_id in rejected_list:#승인 반려 둘다 누른경우 예외
					messages.warning(request,'승인 또는 반려 하나만 체크해 주세요.')
					return redirect('og:admin_menu')

				approved_artist = ArtistEntry.objects.filter(id = artist_entry_id, is_checked = False)
				approved_artist.update(
					is_checked = True,
					is_approved = True
				)
				Artist.objects.create(
					name = approved_artist[0].name,
					email = approved_artist[0].email,
					phone_number = approved_artist[0].phone_number,
					birth_date = approved_artist[0].birth_date,
					gender = approved_artist[0].gender,
					user_id = approved_artist[0].user_id
				)

			for artist_entry_id in rejected_list:#반려 작가 처리
				rejected_artist = ArtistEntry.objects.filter(id = artist_entry_id, is_checked = False)
				rejected_artist.update(
					is_checked = True,
					is_approved = False
				)
			messages.info(request, "승인/반려 처리가 완료되었습니다.")
			return redirect('og:admin_menu')
		else:
			artist_entries = ArtistEntry.objects.all()
			return render(request, 'admin/admin_menu.html', {'artist_entries' : artist_entries})

	else:
		messages.warning(request, "관리자 계정만 접근이 가능합니다.")
		return redirect('og:main')

