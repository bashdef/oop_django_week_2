from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegistrationForm, ApplicationForm, ApplicationStatusForm
from django.views import generic
from .models import Application, AdvUser
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ApplicationFilter
from django.shortcuts import get_object_or_404


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


class ApplicationList(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'catalog/application_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ApplicationFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        return Application.objects.filter(client=self.request.user.id)


class ApplicationCreate(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application_form.html'
    success_url = reverse_lazy('application')

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.client = self.request.user
        fields.save()
        return super().form_valid(form)


class ApplicationDelete(DeleteView):
    model = Application
    success_url = reverse_lazy('application')


@permission_required('catalog.change_application')
def edit_status(request, pk):
    application_status = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST)
        if form.is_valid():
            application_status.status = form.cleaned_data['new_status']
            application_status.save()

            return HttpResponseRedirect(reverse('application'))
    else:
        form = ApplicationStatusForm()

    return render(request, 'catalog/new_status_form.html', {'form': form, 'applicationstatus': application_status})
