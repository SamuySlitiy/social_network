from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.db import models
from .models import User, Friendship, Subscription, PrivateMessage
from .mixins import UserIsOwnerMixin, UserIsProfileOwner
from main_page.forms import *


@login_required
def messages_view(request):
    senters = User.objects.exclude(id=request.user.id)
    return render(request, 'profiles/messages.html', {'senters': senters})

@login_required
def chat_view(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = PrivateMessage.objects.filter(
        (models.Q(senter=request.user, receiver=receiver) | 
         models.Q(senter=receiver, receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'profiles/chat.html', {'receiver': receiver, 'messages': messages})

class UsersListView(ListView):
    model = User
    template_name = "profiles/users.html"
    content_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
    
'''@login_required
class FriendshipListView(ListView):
    model = Friendship
    template_name = 'portfolio/friends.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['requests'] = Friendship.objects.filter(receiver=user.id)
        return context'''