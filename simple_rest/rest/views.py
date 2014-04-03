# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from social.backends.google import GooglePlusAuth
from rest_framework import viewsets, routers, generics, serializers, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from simple_rest.rest.models import CustomUser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from simple_rest.rest.serializers import UserListSerializer, UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    model = CustomUser
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)    
    serializer_class = UserListSerializer

    def get_queryset(self):
        all_users = CustomUser.objects.all()           
        age = int(self.request.QUERY_PARAMS.get('age', 0) or '0')
        
        filtered_result = []
        if age:
            # -- can't do django ORM filtering for dynamic field calculate_age => do manual
            for u in all_users:
                if u.calculate_age() == age:
                    filtered_result.append(u)            
        else:
            filtered_result = all_users
            
        return filtered_result
        
        
class UserSelfView(generics.RetrieveUpdateAPIView):    
    model = CustomUser
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'id'
    parser_classes = (JSONParser,)
    
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        filter['id'] = self.request.user.id
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)        
        return obj
        
    def patch(self, request, format=None):
        obj = self.get_object()
        for k, v in request.DATA.items():
            if k=='age' and int(v):
                # -- can't set concrete date, so set any past date birth fitting age=N
                birthdate = datetime.datetime.today() - datetime.timedelta(days=365*(int(v))+10)
                birthdate = birthdate.date()
                setattr(obj, 'birthdate', birthdate)
                continue
            setattr(obj, k, v)
        obj.save()
        
        serializer = UserSerializer(obj)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        
class UserSingleView(generics.RetrieveAPIView):
    model = CustomUser
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        if self.kwargs['id'] and int(self.kwargs['id']):
            return CustomUser.objects.filter(pk=int(self.kwargs['id']))
        else:
            return []
        

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return render_to_response('home.html', {}, RequestContext(request))


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')
    return render_to_response('home.html', {
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None)
    }, RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)
    return render_to_response('done.html', {
        'user': request.user,
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': scope
    }, RequestContext(request))

    
def signup_email(request):
    return render_to_response('email_signup.html', {}, RequestContext(request))


def validation_sent(request):
    return render_to_response('validation_sent.html', {
        'email': request.session.get('email_validation_address')
    }, RequestContext(request))


def require_email(request):
    if request.method == 'POST':
        request.session['saved_email'] = request.POST.get('email')
        backend = request.session['partial_pipeline']['backend']
        return redirect('social:complete', backend=backend)
    return render_to_response('email.html', RequestContext(request))
