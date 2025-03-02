from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import FormMixin # Позволяет отпровлять сообщения в группах
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import UserIsOwnerMixin
from django.db.models import Avg
from .models import Group, GroupMessage, Rating
from .forms import GroupForm, GroupMessageForm, RatingForm
from django.http import JsonResponse, HttpResponseRedirect

# GROUPS
class GroupListView(ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all().order_by('-is_verified')
        return context

class GroupCreateView(CreateView, LoginRequiredMixin):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_create.html'
    success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class GroupUpdateView(UpdateView, UserIsOwnerMixin):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_update.html'
    success_url = reverse_lazy('group_list')
    
class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'groups/group_delete.html'
    success_url = reverse_lazy('group_list')

# GROUO MESSAGES

class GroupMessageListView(LoginRequiredMixin, ListView):
    model = GroupMessage
    template_name = "groups/group_chat.html"
    context_object_name = "messages"

    def get_queryset(self):
        group = get_object_or_404(Group, id=self.kwargs.get("group_id"))
        return GroupMessage.objects.filter(group=group).select_related("sender").order_by("created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = get_object_or_404(Group, id=self.kwargs.get("group_id"))
        context["form"] = GroupMessageForm()
        return context

class SendMessageView(CreateView):
    model = GroupMessage
    form_class = GroupMessageForm

    def form_valid(self, form):
        group = get_object_or_404(Group, id=self.kwargs.get("group_id"))
        form.instance.sender = self.request.user
        form.instance.group = group
        message = form.save()

        return JsonResponse({
            "id": message.id,
            "sender": message.sender.username,
            "content": message.content,
            "file_url": message.file.url if message.file else None,
            "created_at": message.created_at
        })

class EditMessageView(LoginRequiredMixin, View):
    def post(self, request, message_id):
        message = get_object_or_404(GroupMessage, id=message_id)
        if message.sender != request.user:
            return JsonResponse({'error': 'You do not have permission to edit this message.'}, status=403)

        new_content = request.POST.get('content')
        if new_content:
            message.content = new_content
            message.save()
            return JsonResponse({'id': message.id, 'content': message.content})
        return JsonResponse({'error': 'No content provided.'}, status=400)


class DeleteMessageView(LoginRequiredMixin, View):
    def post(self, request, message_id):
        message = get_object_or_404(GroupMessage, id=message_id)
        if message.sender != request.user:
            return JsonResponse({'error': 'You do not have permission to delete this message.'}, status=403)

        message.delete()
        return JsonResponse({'success': True})
    
# REVIEWS

class RatingListView(ListView):
    model = Rating
    template_name = 'groups/rating_list.html'
    context_object_name = 'ratings'

    def get_queryset(self):
        self.group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        return Rating.objects.filter(group=self.group).order_by('created_at')

    def get_context_data(self, **kwargs):
        average_rating = Rating.objects.filter(group=self.group).aggregate(avg_rating = Avg('rating'))['avg_rating']
        context = super().get_context_data(**kwargs)
        context['group'] = self.group  
        context['average_rating'] = round(average_rating, 2) if average_rating else None
        return context
    
class RatingDetailView(DetailView):
    model = Rating
    template_name = 'groups/rating_detail.html'
    context_object_name = 'rating'

class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = "groups/rating_create.html"
    
    def get_context_data(self, **kwargs):
        self.group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        context = super().get_context_data(**kwargs)
        context['group'] = self.group
        return context
    
    def form_valid(self, form):
        form.instance.group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('rating_list', kwargs={'group_id': self.object.group.id})
        
class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'groups/rating_update.html'

    def get_context_data(self, **kwargs):
        self.group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        context = super().get_context_data(**kwargs)
        context['group'] = self.group
        return context

    def get_success_url(self):
        return reverse_lazy('rating_list', kwargs={'group_id': self.object.group.id})

class RatingDeleteView(LoginRequiredMixin, DeleteView):
    model = Rating
    template_name = 'groups/rating_delete.html'

    def get_success_url(self):
        return reverse_lazy('rating_list', kwargs={'group_id': self.object.group.id})
