from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth, messages

from .models import Artist, ArtistEntry
from .forms import ArtistEntryForm

from validator import phone_number_validate, date_validate

def main(request):
	return render(request, 'index.html', {})

def artist_entry(request):
	if request.user.is_authenticated:

		if ArtistEntry.objects.filter(user_id = request.user.id).exists():
				messages.info(request, "이미 등록된 작가거나 작가 등록 심사중 입니다.")
				return redirect('og:main')

		if request.method == 'POST':
			form = ArtistEntryForm(request.POST)
			if form.is_valid():

				if phone_number_validate(form.data['phone_number']):
					messages.info(request, "전화번호 형식을 000-0000-0000 과 같이 입력하세요.")
					return redirect('og:artist_entry')

				if date_validate(form.data['birth_date']):
					messages.info(request, "생년월일 형식을 0000-00-00 과 같이 입력하세요.")
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
			return redirect('og:main')

		else: #GET일때
			form = ArtistEntryForm()
			return render(request, 'artist_entry.html', {'form' : form})

	else: #로그인 안했을때
		messages.warning(request, "로그인 창으로 이동합니다.")
		return redirect('accounts:login')

def artist_menu(request):
	if Artist.objects.filter(user_id = request.user.id).exists():
		return render(request, 'artist_menu.html', {})
	messages.info(request, "아직 작가에 등록하지 않으셨거나 작가 승인이 되지 않았습니다.")
	return redirect ('og:main')