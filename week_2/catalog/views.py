from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm
from django.views import generic
from .models import Application
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'catalog/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'catalog/register.html', {'user_form': user_form})


@login_required()
def profile(request):
    return render(request, 'catalog/profile.html')


class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'catalog/application_list.html'

    def get_queryset(self):
        return Application.objects.order_by('status')


class ApplicationCreateView(CreateView):
    model = Application
    fields = ['name', 'summary', 'caterogy', 'image']
