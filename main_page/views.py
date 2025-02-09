from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .forms import *
from profiles.utils import create_notification

def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main-page')
    else:
        form = UserForm()

    return render(request, 'main_page/register.html', context = {'form': form})

def login_view(request):
    if request.method == "POST":
        form = UserAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main-page')
            else: 
                messages.error(request, "Invalid Data: Login or Password")
                return redirect('login')
    else:
        form = UserAuthForm()

    return render(request, 'main_page/login.html', context = {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

class IndexPage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('created_at')
        context['notes'] = Note.objects.filter(author=self.request.user).order_by('created_at')
        return context

# POSTS & LIKES

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "main_page/post_create.html"
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostListView(ListView):
    model = Post
    template_name = "main_page/post_list.html"
    context_object_name = 'posts'
    queryset = Post.objects.all().order_by('created_at')

class PostDetailView(DetailView):
    model = Post
    template_name = "main_page/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('created_at')
        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "main_page/post_delete.html"
    success_url = reverse_lazy('main-page') 

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
class LikeListView(ListView):
    model = Like
    template_name = "main_page/like_list.html"
    context_object_name = "likes"

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Like.objects.filter(post=post)

class LikeCreateView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            create_notification(post.user, request.user, 'like', f"{request.user.username} liked your post.")
        
        return JsonResponse({'message': 'Liked successfully', 'likes_count': post.likes.count()})


class LikeDeleteView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        like = Like.objects.filter(user=request.user, post=post)

        if like.exists():
            like.delete()
            return JsonResponse({'message': 'Unliked successfully', 'likes_count': post.likes.count()})
        
        return JsonResponse({'message': 'Not liked yet'}, status=400)

# NOTES

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "main_page/note_create.html"
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NoteListView(ListView):
    model = Note
    template_name = "main_page/note_list.html"
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user).order_by('created_at')

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = "main_page/note_delete.html"
    success_url = reverse_lazy('note-list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)
    
# COMMENTS
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "main_page/comment_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('comment-list', kwargs={'post_id': self.object.post.id})

class CommentListView(ListView):
    model = Comment
    template_name = "main_page/comment_list.html"
    context_object_name = 'comments'

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(post=self.post).order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post  # Make sure `post` is available for the template
        return context
    
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'main_page/comment_update.html'

    def get_success_url(self):
        return reverse_lazy('comment-list', kwargs={'post_id': self.object.post.id})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "main_page/comment_delete.html"
    success_url = reverse_lazy('comment-list')
    
    def get_success_url(self):
        return reverse_lazy('comment-list', kwargs={'post_id': self.object.post.id})