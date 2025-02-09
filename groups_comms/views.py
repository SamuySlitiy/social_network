from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormMixin # Позволяет отпровлять сообщения в группах
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import UserIsOwnerMixin
from .models import Group, GroupMessage, Rating
from .forms import GroupForm, GroupMessageForm, RatingForm
from django.http import JsonResponse

# GROUPS
class GroupListView(ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'groups'
    queryset = Group.objects.all().order_by('is_verified')

class GroupCreateView(CreateView, LoginRequiredMixin):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_create.html'
    success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

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

class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = GroupMessage.objects.order_by("-sent_at")
        context['message_form'] = GroupMessageForm()
        return context

class GroupMessageListView(LoginRequiredMixin, ListView):
    model = GroupMessage
    template_name = "groups/group_detail.html"
    context_object_name = "messages"

    def get_queryset(self):
        group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        return group.messages.all().order_by("-sent_at")

class GroupMessageCreateView(LoginRequiredMixin, CreateView):
    model = GroupMessage
    form_class = GroupMessageForm
    template_name = "groups/group_detail.html"

    def form_valid(self, form):
        group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        form.instance.sender = self.request.user
        form.instance.group = group
        self.object = form.save()
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
            return JsonResponse({
                'sender': self.object.sender.username,
                'content': self.object.content,
                'timestamp': self.object.timestamp.strftime("%Y-%m-%d %H:%M"),
                'file': self.object.file.url if self.object.file else None
            })
        
        return redirect('group_detail', pk=group.id)

class GroupMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = GroupMessage
    form_class = GroupMessageForm
    template_name = "groups/group_message_edit.html"

    def get_success_url(self):
        return reverse_lazy("group_detail", kwargs={"pk": self.object.group.pk})

class GroupMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = GroupMessage
    template_name = "groups/group_message_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("group_detail", kwargs={"pk": self.object.group.pk})

    
# REVIEWS

class RatingListView(ListView):
    model = Rating
    template_name = 'groups/rating_list.html'
    context_object_name = 'ratings'

    def get_queryset(self):
        self.group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        return Rating.objects.filter(group=self.group).order_by('created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = self.group 
        return context

class RatingCreateView(LoginRequiredMixin, CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'groups/rating_create.html'

    def form_valid(self, form):
        self.group = get_object_or_404(Group, pk=self.kwargs['group_id'])
        form.instance.user = self.request.user
        form.instance.group = self.group 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.object.group.pk})

        
class RatingUpdateView(LoginRequiredMixin, UpdateView):
    model = Rating
    form_class = RatingForm
    template_name = 'groups/rating_update.html'

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.object.group.pk})

class RatingDeleteView(LoginRequiredMixin, DeleteView):
    model = Rating
    template_name = 'groups/rating_delete.html'

    def get_success_url(self):
        return reverse_lazy('group_detail', kwargs={'pk': self.object.group.pk})
