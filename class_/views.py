from django.shortcuts import render, redirect
from .models import Package, Student
from .forms import RegisterForm
from django.contrib import messages

# Create your views here.
def home(request):
	return render(request, 'index.html', {})

def contact(request):
	return render(request, 'contact.html', {})

def classes(request):
	form=RegisterForm()
	if request.method=='POST':
		form=RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, ("You have successfully registered"))
			return redirect('classes')
	else:
		form=RegisterForm()
		return render(request, 'classes.html', {'form':form})

def login_user(request):
	return render(request, 'login.html', {})

def register(request):
	return render(request, 'register.html', {})