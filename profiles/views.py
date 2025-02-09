from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView, View
from django.db import models
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Follow, PrivateMessage, Notification
from .mixins import UserIsOwnerMixin, UserIsProfileOwner
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
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username
        context['first_name'] = self.user.user_first_name()
        context['last_name'] = self.user.user_last_name()
        context['email'] = self.user.user_email()
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

    def get_object(self, queryset=None):
        return get_object_or_404(Follow, pk=self.kwargs['pk'])

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
        return JsonResponse({"followed": True})  # Followed

    return JsonResponse({"error": "Invalid request"}, status=400)

# MESSAGES

@login_required
def chat_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = PrivateMessage.objects.filter(
        senter=request.user, receiver=receiver
    ) | PrivateMessage.objects.filter(
        senter=receiver, receiver=request.user
    ).order_by("sent_at")

    if request.method == "POST":
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.senter = request.user
            message.receiver = receiver
            message.save()
            return JsonResponse({
                "senter": message.senter.username,
                "text": message.text,
                "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M:%S")
            }) 

    else:
        form = PrivateMessageForm()

    return render(request, "messages.html", {
        "receiver": receiver,
        "messages": messages,
        "form": form
    })

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(PrivateMessage, id=message_id, sender=request.user)
    
    if request.method == "POST":
        message.delete()
        return JsonResponse({"success": True}) 

    return JsonResponse({"error": "Invalid request"}, status=400)

# NOTIFICATIONS

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False).order_by('-created_at')

class MarkNotificationAsReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'message': 'Notifications marked as read'})