from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.template import engines
from django.urls import reverse
from django.views import View
from django_registration.backends.one_step.views import RegistrationView

from main.forms import KekPassForm, RegistrationForm
from main.models import KekPass


def render_kekpass(kekpass: KekPass) -> str:
    from os.path import join, dirname

    template = join(dirname(__file__), 'templates/kekpass.html')
    with open(template, 'r', encoding='utf-8') as template:
        template = template.read()
        context = {
            'pk': kekpass.pk,
            'host': kekpass.host,
            'password': kekpass.password,
        }
        return template.format(**context)


class ExtendedLoginView(LoginView):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        response = super(LoginView, self).post(request, *args, **kwargs)
        if not request.user.is_authenticated:
            messages.error(request, 'Ошибка авторизации')
        return response


class ExtendedRegistrationView(RegistrationView):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = RegistrationForm(request.POST)
        for scope in form.errors.values():
            for error in list(scope):
                messages.error(request, error)
        response = super().post(request, *args, **kwargs)
        return response


class IndexView(View):
    context = {'pagename': 'Главная'}

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'index.html', self.context)


class StorageView(View, LoginRequiredMixin):
    context = {'pagename': 'Хранилище'}

    def get(self, request: HttpRequest) -> HttpResponse:
        self.context['form'] = KekPassForm()
        self.context['kekpasses'] = KekPass.objects.filter(user=request.user)
        return render(request, 'storage.html', self.context)

    def post(self, request: HttpRequest) -> HttpResponsePermanentRedirect:
        form = KekPassForm(request.POST, instance=request.user)
        if form.is_valid():
            KekPass(
                host=form.cleaned_data['host'],
                password=form.cleaned_data['password'],
                user=request.user,
            ).save()
        return redirect(reverse('storage'))


class KekpassView(View, LoginRequiredMixin):
    def get(self, request: HttpRequest, pk: int) -> HttpResponsePermanentRedirect:
        kekpass = KekPass.objects.filter(user=request.user, pk=pk)
        if kekpass.exists():
            kekpass = kekpass.get()
            engine = engines['jinja2']
            template = engine.from_string(render_kekpass(kekpass))
            return HttpResponse(template.render({}, request))
        return redirect(reverse('storage'))


class RemoveKekpassView(View, LoginRequiredMixin):
    def get(self, request: HttpRequest, pk: int) -> HttpResponsePermanentRedirect:
        kekpass = KekPass.objects.filter(user=request.user, pk=pk)
        if kekpass.exists():
            kekpass.get().delete()
        return redirect(reverse('storage'))
