from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, TemplateView, View
from django.db import models
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Follow, PrivateMessage, Notification
from .forms import *
from .utils import create_notification
    
# USERS

class UsersListView(ListView):
    model = User
    template_name = "profiles/users.html"
    context_object_name = "users"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return User.objects.filter(
                models.Q(username__icontains=query) |
                models.Q(email__icontains=query)
            )
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class UserDetailView(DetailView):
    model = User
    template_name = 'profiles/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        self.user = get_object_or_404(User, pk=self.kwargs['pk'])
        followers = Follow.objects.filter(is_followed=self.user).select_related("is_following")
        following = Follow.objects.filter(is_following=self.user).select_related("is_followed")
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username
        context['first_name'] = self.user.user_first_name()
        context['last_name'] = self.user.user_last_name()
        context['email'] = self.user.user_email()
        context["followers"] = followers 
        context["following"] = following  # List of Follow objects where user follows others

        return context

    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'profiles/user_update.html'

    def form_valid(self, form):
        self.object = form.save()
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX
            return JsonResponse({"message": "Profile updated successfully"})
        
        return super().form_valid(form)

# FOLLOWS
class FollowListView(LoginRequiredMixin, ListView):
    model = Follow
    template_name = "profiles/follow_list.html"
    context_object_name = 'follows'
    
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Follow.objects.filter(
            models.Q(is_following=user) | 
            models.Q(is_followed=user)
        ).order_by('-created_at')

class FollowDetailView(LoginRequiredMixin, DetailView):
    model = Follow
    template_name = "profiles/follow_detail.html"
    context_object_name = 'follow'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Follow.objects.filter(is_following=user).order_by('-created_at')
    

@login_required
def toggle_follow(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_to_follow = get_object_or_404(User, id=user_id)

        if request.user == user_to_follow:
            return JsonResponse({"error": "You cannot follow yourself"}, status=400)

        follow, created = Follow.objects.get_or_create(is_following=request.user, is_followed=user_to_follow)

        if not created:
            follow.delete()
            return JsonResponse({"followed": False})  # Unfollowed
        create_notification(user_to_follow, request.user, 'follow', f"{request.user.username} is now following you!")
        return JsonResponse({"followed": True})  # Followed

    return JsonResponse({"error": "Invalid request"}, status=400)

# MESSAGES

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = PrivateMessage
    fields = ["text"]

    def form_valid(self, form):
        form.instance.senter = self.request.user
        form.instance.receiver = get_object_or_404(User, id=self.kwargs["receiver_id"])
        message = form.save()

        return JsonResponse({
            "senter": message.senter.username,
            "text": message.text,
            "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M"),
        })
    
class MessageListView(LoginRequiredMixin, ListView):
    template_name = "profiles/messages.html"
    context_object_name = "messages"

    def get_queryset(self):
        receiver = get_object_or_404(User, pk=self.kwargs["receiver_id"])
        return PrivateMessage.objects.filter(
            senter=self.request.user, receiver=receiver
        ) | PrivateMessage.objects.filter(
            senter=receiver, receiver=self.request.user
        ).order_by("sent_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receiver"] = get_object_or_404(User, pk=self.kwargs["receiver_id"])
        return context

class ChatListView(LoginRequiredMixin, ListView):
    template_name = "profiles/chats.html"
    context_object_name = "chat_users"

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)  # Show all users except self

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(PrivateMessage, id=message_id, senter=request.user)
    
    if request.method == "POST":
        message.delete()
        return JsonResponse({"success": True}) 

    return JsonResponse({"error": "Invalid request"}, status=400)

# NOTIFICATIONS

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "profiles/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-created_at')

class MarkNotificationAsReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'message': 'Notifications marked as read'})