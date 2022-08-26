from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_repeat']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],)
            auth.login(request, user)
            return redirect('/main')
        return render(request, 'signup.html')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/main')
        else: #로그인 실패
            messages.warning(request, "아이디 또는 비밀번호를 다시 한번 확인해 주세요.")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/main')
