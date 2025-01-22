from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.db import models
from django.urls import reverse_lazy
from .models import User, Friendship, Subscription, PrivateMessage
from django.contrib.auth.mixins import LoginRequiredMixin #, UserPassesTestMixin
from .mixins import UserIsOwnerMixin, UserIsProfileOwner
from .forms import *
    
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
    template_name = 'profiles/user_detal.html'
    context_object_name = 'user_profile'

class UserUpdateView(LoginRequiredMixin, UserIsProfileOwner, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'profiles/user_update.html'
    success_url = reverse_lazy('')

    def get_object(self, queryset=None):
        return self.request.user

# FRIENDS
    
class FriendshipListView(LoginRequiredMixin, ListView):
    model = Friendship
    template_name = 'profiles/friends.html'
    context_object_name = 'friendships'

    def get_queryset(self):
        return self.request.user.get_friends()

class FriendshipCreateView(LoginRequiredMixin, CreateView):
    model = Friendship
    form_class = FriendshipForm
    template_name = 'profiles/request_friendship.html'
    success_url = reverse_lazy('friends-list')

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)
    
class FriendshipDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Friendship
    template_name = 'profiles/friendship_confirm_delete.html'
    success_url = reverse_lazy('friends-list')

# SUBSCRIPTIONS

class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = 'profiles/subscribtions.html'
    context_object_name = 'subscriptions'

    def get_queryset(self):
        return self.request.user.subscriptions.all()

class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    template_name = 'profiles/request_subscribtion.html'
    success_url = reverse_lazy('subscription-list')

    def form_valid(self, form):
        form.instance.subscriber = self.request.user
        return super().form_valid(form)

class SubscriptionDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Subscription
    template_name = 'profiles/subscription_confirm_delete.html'
    success_url = reverse_lazy('subscriptions-list')
    

# MESSAGES

class PrivateMessageListView(LoginRequiredMixin, ListView):
    model = PrivateMessage
    template_name = 'profiles/private_message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return PrivateMessage.objects.filter(receiver=self.request.user)


class PrivateMessageCreateView(LoginRequiredMixin, CreateView):
    model = PrivateMessage
    form_class = PrivateMessageForm
    template_name = 'profiles/private_message_form.html'
    success_url = reverse_lazy('private-message-list')

    def form_valid(self, form):
        form.instance.senter = self.request.user
        return super().form_valid(form)
    
class PrivateMessageDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = PrivateMessage
    template_name = 'profiles/private_message_confirm_delete.html'
    success_url = reverse_lazy('private-message-list')

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