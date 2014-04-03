# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers, generics
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

from rest.serializers import UserListSerializer, UserSerializer
from rest.models import CustomUser
from rest.views import UserSelfView, UserSingleView, UserViewSet


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^/?$', 'simple_rest.rest.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'simple_rest.rest.views.signup_email'),
    url(r'^email-sent/', 'simple_rest.rest.views.validation_sent'),
    url(r'^login/$', 'simple_rest.rest.views.home'),
    url(r'^logout/$', 'simple_rest.rest.views.logout'),
    url(r'^done/$', 'simple_rest.rest.views.done', name='done'),
    url(r'^email/$', 'simple_rest.rest.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    
    url(r'^api/users/(?P<id>[0-9]+)/?$', UserSingleView.as_view(), name='user-single'),
    url(r'^api/user/$', UserSelfView.as_view(), name='user-self'),    
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns += patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/login/?$', RedirectView.as_view(url='/', permanent=False), name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
