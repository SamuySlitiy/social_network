from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from .forms import *

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

@login_required
class PostCreateView(CreateView):
    model = Post
    template_name = "main_page/index.html"
    fields = ['author', 'content', 'image']
    widgets = {
        'created_at': forms.DateInput(attrs={'type': 'date'})
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostListView(ListView):
    model = Post
    template_name = "main_page/index.html"
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context

class PostDeleteView(DeleteView):
    model = Post
    template_name = "main_page/index.html"
    success_url = reverse_lazy('main_page/index.html')

class NoteCreateView(CreateView):
    model = Note
    template_name = "main_page/index.html"
    fields = ['author', 'content']
    widgets = {
        'created_at': forms.DateInput(attrs={'type': 'date'})
    }

class NoteDeleteView(DeleteView):
    model = Note
    template_name = "main_page/index.html"
    success_url = reverse_lazy('main_page/index.html')

class NoteListView(ListView):
    model = Note
    template_name = "main_page/index.html"
    context_object_name = 'note'

class CommentCreateView(CreateView):
    model = Comment
    template_name = "main_page/post.html"
    context_object_name = 'comments'
    fields = ['author', 'content']
    widgets = {
        'created_at': forms.DateInput(attrs={'type': 'date'})
    }

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = "main_page/post.html"
    success_url = reverse_lazy('main_page/index.html')

class CommentListView(ListView):
    model = Post
    template_name = "main_page/post.html"
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context