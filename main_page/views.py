from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.db import models
from .models import Post, Comment
from .forms import UserForm, UserAuthForm

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()

    return render(request, template_name='main_page/register.html',context = {'form': form})

def login(request):
    if request.method == "POST":
        form = UserAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else: 
                messages.error(request, "Invalid Data: Login or Password")
        else:
            form = UserAuthForm()

    return render(request, template_name='main_page/login.html', context = {'form': form})

def logout(request):
    logout(request)
    return redirect('home')