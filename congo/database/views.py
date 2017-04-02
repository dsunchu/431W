from django.shortcuts import render
from django.http import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
# Create your views here.

'''
FUNCTIONALITY
-creating users
-creating suppliers
-user login
-viewing user profile

'''

'''
action="http://localhost:8000/create_user/details/"
'''
def create_user(request):
    print('in create_user')
    # if post request came
    if request.method == "POST":
       #user = request.user
       form = registered_user_form(request.POST)
       if form.is_valid():
           request.session['username'] = form['username'].value()
           form.save()
           user = User.objects.create_user(username=form['username'].value(),password=form['password'].value())
           user.save()
           registered_user = RegisteredUser.objects.get(name=form['name'].value())
           registered_user.user = user
           registered_user.save()
           return redirect('database:view_profile')
           #return render(request,'database/create_user_info.html')
    else:
        form = registered_user_form()
    return render(request, 'database/create_user.html', {'form': form})
'''
def create_user_info(request):
    if request.method == "POST":
        print(request.session['username'])
        form = registered_user_form(request.POST)
        if form.is_valid():
            form.save()
            user=User.objects.get(username = request.session['username'])
            registered_user = RegisteredUser.objects.get(name=form['name'].value())
            registered_user.user=user   #link User model with RegisteredUser model
            registered_user.save()
            #return redirect('view_profile',pk=post.user)
            return redirect('database:view_profile')
    else:
        form = registered_user_form()
    return render(request,'database/create_user_info.html',{'form':form})

'''
def view_users(request):
    registered_users = RegisteredUser.objects.all()
    return render(request,'database/display_users.html', { 'registered_users': registered_users})

#user_name pkey
def view_profile(request):
    user_name = request.session['username']
    user = User.objects.get(username=user_name)
    model_user = RegisteredUser.objects.get(user=user)
    model_user.username = user_name
    return render(request,'database/create_user_profile.html',{'user':model_user})

def create_supplier(request):
    if request.method == "POST":
        form = supplier_form(request.POST)
        if form.is_valid():
            form.save()
            request.session['supplier_id'] = form['supplier_id'].value()
            return redirect('database:supplier_profile')
    else:
        form = supplier_form()
    return render(request,'database/create_supplier.html',{'form':form})

def supplier_profile(request):
    supplier_ID = request.session['supplier_id']
    supplier_info = supplier.objects.get(supplier_id=supplier_ID)
    return render(request,'database/supplier_profile.html',{'supplier':supplier_info})

#renders userprofile
@login_required(login_url='http://localhost:8000/login/')
def view_user_profile(request,user_name):
    #username = request.POST.username
    if request.user.is_authenticated:
        print(request.session['username'])
        model_user = User.objects.get(username=request.session['username'])
        registered_user = RegisteredUser.objects.get(user = model_user)
        registered_user.username = request.session['username']
        return render(request,'database/user_profile.html',{'registered_user':registered_user})

#displays login page
#only logs in superusers
def login_user(request):
    logout(request)
    username = password = ''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #user_url = 'http://localhost:8000/u/' + username + '/'
                request.session['username'] = username
                return redirect('http://localhost:8000/')
    return render(request,'database/login.html')


def index_page(request):
    return render(request,'database/test.html')

