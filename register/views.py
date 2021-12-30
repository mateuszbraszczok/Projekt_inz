from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = RegisterForm()
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/login")
    
    context = {"form":form}
    return render(request, "register/register.html", context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                nextPage = request.GET.get('next')
                print(nextPage)
                if nextPage is not None:
                    return redirect(nextPage)
                else:
                    print('ala ma kota')
                    return redirect('/projekt')
            else:
                messages.info(request, 'Username OR password is incorrect')
        form = LoginForm()
        context = {"form":form}
        return render(request, "login/login.html", context)

def logoutUser(request):
	logout(request)
	return redirect('/login')