from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormMixin # Позволяет отпровлять сообщения в группах
from django.contrib.auth.mixins import LoginRequiredMixin
from profiles.mixins import UserIsOwnerMixin
from .models import Group, GroupMessage
from .forms import GroupForm, GroupMessageForm

# GROUPS
class GroupListView(ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'
class GroupCreateView(CreateView, LoginRequiredMixin):
    model = Group
    form_class = GroupForm
    template_name = 'group_form.html'
    success_url = reverse_lazy('groups_comms:group-list')

class GroupUpdateView(UpdateView, LoginRequiredMixin, UserIsOwnerMixin):
    model = Group
    form_class = GroupForm
    template_name = 'group_form.html'
    success_url = reverse_lazy('groups_comms:group-list')

class GroupDeleteView(DeleteView, LoginRequiredMixin, UserIsOwnerMixin):
    model = Group
    template_name = 'group_confirm_delete.html'
    success_url = reverse_lazy('groups_comms:group-list')

# GROUO MESSAGES
class GroupDetailView(DetailView, LoginRequiredMixin, FormMixin):
    model = Group
    form_class = GroupMessageForm
    template_name = 'group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_messages'] = self.object.messages.order_by('sent_at')
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            message = form.save(commit=False)
            message.group = self.object
            message.sender = request.user
            message.save()
            return redirect('groups_comms:group_detail', pk=self.object.pk)
        else:
            return self.form_invalid(form)

class GroupMessageUpdateView(UpdateView, LoginRequiredMixin):
    model = GroupMessage
    form = GroupMessageForm 
    template_name = 'group_message_form.html'

    def get_success_url(self):
        return reverse_lazy('groups_comms:group_detail', kwargs={'pk': self.object.group.pk})

    # UserIsOwner
    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.sender != request.user:
            return redirect('groups_comms:group_detail', pk=message.group.pk)
        return super().dispatch(request, *args, **kwargs)
    
class GroupMessageDeleteView(DeleteView, LoginRequiredMixin):
    model = GroupMessage
    template_name = 'group_message_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('group_comms:group_detail', kwargs={'pk': self.object.group.pk})

    # UserIsOwner
    def dispatch(self, request, *args, **kwargs):
        message = self.get_object()
        if message.sender != request.user:
            return redirect('group_comms:group_detail', pk=message.group.pk)
        return super().dispatch(request, *args, **kwargs)