from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from main import forms
from main.views import (ExtendedLoginView, ExtendedRegistrationView, IndexView,
                        KekpassView, RemoveKekpassView, StorageView)

registration = [
    path(
        'register/',
        ExtendedRegistrationView.as_view(
            form_class=forms.RegistrationForm,
            template_name='registration/registration.html',
            success_url=reverse_lazy('index'),
        ),
        name='register',
    ),
    path(
        'login/',
        ExtendedLoginView.as_view(
            form_class=forms.AuthenticationForm,
            template_name='registration/authentication.html',
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
]

main = [
    path('', IndexView.as_view(), name='index'),
    path('store/', StorageView.as_view(), name='storage'),
    path('store/<int:pk>/', KekpassView.as_view(), name='kekpass'),
    path('store/<int:pk>/remove/', RemoveKekpassView.as_view(), name='remove'),
]

urlpatterns = []
urlpatterns.extend(registration)
urlpatterns.extend(main)
