from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import UserIsOwnerMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
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

@login_required
def logout(request):
    logout(request)
    return redirect('home')

# POSTS

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "main_page/index.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('created_at')
        context['notes'] = Note.objects.filter(author=self.request.user).order_by('created_at')
        return context

class PostListView(ListView):
    model = Post
    template_name = "main_page/index.html"
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('created_at')


class PostDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Post
    template_name = "main_page/posts.html"
    success_url = reverse_lazy('main_page:index') 

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# NOTES

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    model = NoteForm
    template_name = "main_page/index.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NoteListView(ListView):
    model = Note
    template_name = "main_page/index.html"
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user).order_by('created_at')

class NoteDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Note
    template_name = "main_page/index.html"
    success_url = reverse_lazy('main_page:index')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    
# COMMENTS
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form = CommentForm
    template_name = "main_page/posts.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

class CommentListView(ListView):
    model = Comment
    template_name = "main_page/posts.html"
    context_object_name = 'comments'

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=post).order_by('created_at')
    
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'main_page/posts.html'

    def get_success_url(self):
        return reverse_lazy('', kwargs={'pk': self.object.post.id})

class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = "main_page/posts.html"

    def get_success_url(self):
        return reverse_lazy('posts.html')

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)