from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import strip_tags
from .models import *
from .forms import *

# Create your views here.
def index(request):
    messages_count = Message.objects.all().count()
    context = {
        'messages_count':messages_count
        }
    return render(request, 'portfolio/index.html', context)

# ******************* SEND VIEW *****************************
def send(request):
    if request.method =='POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message successfully sent")
            return redirect(request.META.get("HTTP_REFERER"))

        else:
            for field, error in form.errors.items():
                error = strip_tags(error)
                messages.error(request,f"{field}: {error}")
                return redirect(request.META.get("HTTP_REFERER"))



# ******************* ADMIN PAGE VIEW *****************************
@login_required(login_url="portfolio:admin_login")   
def dashboard(request):
    return render(request, 'dashboard/home.html')


# ******************* ADMIN MESSAGE *****************************
@login_required(login_url="portfolio:admin_login")   
def message(request):
    messages_count = Message.objects.all().count()
    messages = Message.objects.all().order_by("-id")
    context = {
        'messages': messages,
        'messages_count':messages_count
    }
    return render(request, 'dashboard/message.html', context)

# ******************* ADMIN LOGIN *****************************
def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_staff and user.is_superuser:
            login(request, user)
            return redirect('portfolio:dashboard')

        else:
            messages.error(request, "Invalid Credential")
            return redirect("portfolio:admin_login")

    return render(request, 'dashboard/login.html')

# ******************* ADMIN LOGOUT  VIEW *****************************
def log_out(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect("portfolio:admin_login")
