from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
	
def confirmUser(request):
	username = request.GET['username']
	password = request.GET['password']
	user = auth.authenticate(username=username,password=password)
	if user:
		auth.login(request,user)
		return HttpResponse('yes')
	return HttpResponse('no')