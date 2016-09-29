import requests
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import status
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.


def login_auth(request, template_name):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            url = ''.join(['http://', get_current_site(request).domain, reverse('fetch_token')])
            response = requests.post(url, json={"username":username, "password":password})
            return HttpResponse(response.text, content_type = 'application/json', status=status.HTTP_200_OK )
        else:
            return HttpResponseBadRequest()
    else:
        if isinstance(request.user,User):
            return redirect(reverse('homepage'))
        else:
            context = {}
            return TemplateResponse(request, template_name, context)