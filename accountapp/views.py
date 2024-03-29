from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountUpdateForm
from accountapp.models import NewModel


def hello_world(request):
    # return HttpResponse('Hello World!')
    if request.method == "POST":
        input_data = request.POST.get('input_data')
        new_model = NewModel()
        new_model.text = input_data
        new_model.save()
        return HttpResponseRedirect(reverse('accountapp:hello_world'))
    new_model_list = NewModel.objects.all()
    return render(request, 'accountapp/hello_world.html', context={'new_model_list':new_model_list})

class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

has_ownership = [account_ownership_required, login_required]

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = User
    form_class = AccountUpdateForm
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world') # 나중에 경로 변경
    template_name = 'accountapp/update.html'
    # def post(self, request, *args, **kwargs):
    #     if request.user == self.object:
    #         return super().post(request, *args, **kwargs)
    #     else:
    #         return HttpResponseForbidden()

@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/delete.html'