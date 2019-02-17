from django.conf.urls import url
from django.urls import path, re_path

from accounts import views

urlpatterns = [
    # path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('acc-settings/<int:pk>/', views.UpdateAccountView.as_view(), name='acc-update'),
]
