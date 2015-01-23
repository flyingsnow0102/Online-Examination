from django.views.generic.base import View
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

class Home(View):
    def get(self, request, *args, **kwargs):

        context = {
            
        }
        return render(request, 'home.html',context)# Create your views here.
class Login(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return render_to_response('home.html',{},RequestContext(request))

    def post(self,request,*args,**kwargs):
        if request.POST.get('username', '') and request.POST.get('password',''):
            username = request.POST.get('username', '')
            user = authenticate(username=request.POST.get('username', ''), password=request.POST.get('password',''))
           
        elif request.POST.get('registration_no','') and request.POST.get('hallticket_no','') and request.POST.get('password',''):
            username = request.POST.get('registration_no','') + request.POST.get('hallticket_no','')
            user = authenticate(username=username, password=request.POST.get('password',''))
        
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'home.html',context)
        context = {
         'Success_message': 'Welcome '+username
        }
        return HttpResponseRedirect(reverse('home'))

class Logout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))

class ResetPassword(View):

    def get(self, request, *args, **kwargs):

        user = User.objects.get(id=kwargs['user_id'])
        context = {
            'user_id': user.id
        }
        return render(request, 'reset_password.html', context)

    def post(self, request, *args, **kwargs):

        context = {}
        user = User.objects.get(id=kwargs['user_id'])
        if request.POST['password'] != request.POST['confirm_password']:
            context = {
                'user_id': user.id,
                'message': 'Password is not matched with Confirm Password',
            }
            return render(request, 'reset_password.html', context)
        if len(request.POST['password']) > 0 and not request.POST['password'].isspace():
            user.set_password(request.POST['password'])
        user.save()
        if user == request.user:
            logout(request)
            return HttpResponseRedirect(reverse('home'))  
        else:
            user_type = user.userprofile_set.all()[0].user_type 
            return HttpResponseRedirect(reverse('users', kwargs={'user_type': user_type}))