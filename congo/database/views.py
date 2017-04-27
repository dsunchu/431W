from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from django.db.models import Q
import random
from django.http import HttpResponseRedirect
from django.contrib.sessions.middleware import SessionMiddleware
from itertools import chain
import operator
import operator
import multiprocessing
import datetime
from .tasks import add
# Create your views here.

#cookies / cookiemonster admin
#hungry/hungry registered

'''
//////////////////////////////////////////////////////////////////////////////////
USERS BEGIN
-creating users
-creating suppliers
-user login
-viewing user profile
-supplier login -> not started
/////////////////////////////////////////////////////////////////////////////////
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
    newitems = sale_items.objects.all()[:4]
    neatproducts = sale_items.objects.all()[4:10]
    topproducts1 = sale_items.objects.all()[10:13]
    topproducts2 = sale_items.objects.all()[13:16]
    topproducts3 = sale_items.objects.all()[16:19]
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            cat = form.cleaned_data['category']
            search = form.cleaned_data['search']
            query = sale_items.objects.filter((Q(category__category_name = cat) | Q(category__parent_category = cat)) & (Q(item_name__icontains=search) | Q(description__icontains=search)))

            return render(request, 'database/search_results.html', {'query':query})
        else:
            form = search_form()

    if request.user.is_authenticated() == 1:
        form = search_form()
        print("logged in user ",request.user.username)
        r = RegisteredUser.objects.get(user__username=request.user.username)
        return render(request,'database/test.html',{'registered_user':r, 'form':form, 'newitems':newitems, 'neatproducts':neatproducts, 'topproducts1':topproducts1, 'topproducts2':topproducts2,'topproducts3':topproducts3})
    else:
        form = search_form()
        return render(request, 'database/test.html', {'form':form})


@login_required(login_url='http://localhost:8000/login/')
def add_credit_card(request):
    if request.method == "POST":
        form = credit_card_form(request.POST)
        if form.is_valid():
            #find corresponding user, link user to creditcard
            r = RegisteredUser.objects.get(user__username=request.user.username)
            if form.save():
                credit_card = credit_cards.objects.get(card_number=form['card_number'].value())
                credit_card.user = r
                credit_card.save()
                return render(request, 'items/upload_success.html')
            else:
                return render(request, 'items/upload_fail.html')
    else:
        form = credit_card_form
    return render(request,'database/add_credit_card.html',{'form':form})

@login_required(login_url='http://localhost:8000/login/')
def add_address(request):
    if request.method == "POST":
        form = address_form(request.POST)
        if form.is_valid():
            form.save()
            #find corresponding user, link user to creditcard
            r = RegisteredUser.objects.get(user__username=request.user.username)
            #if form.save():
            street = form['street'].value()
            city = form['city'].value()
            zip_code = form['zip_code'].value()
            address = addresses.objects.filter(street=street,city=city,zip_code=zip_code)
            address.user = r
            address.update()
            return render(request, 'items/upload_success.html')
            #else:
                #return render(request, 'items/upload_fail.html')
    else:
        form = address_form
        #use same template as add creditcard
    return render(request,'database/add_address.html',{'form':form})

def base(request):
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            cat = form.cleaned_data['category']
            search = form.cleaned_data['search']
            query = sale_items.objects.filter(Q(category__category_name = cat) | Q(category__parent_category = cat) & (Q(item_name__icontains=search) | Q(description__icontains=search)))

            return render(request, 'database/base.html', {'query':query})
        else:
            form = search_form()

@login_required(login_url='http://localhost:8000/login/')
def add_email(request):
    if request.method == "POST":
        form = email_form(request.POST)
        if form.is_valid():
            #find corresponding user, link user to creditcard
            r = RegisteredUser.objects.get(user__username=request.user.username)
            if form.save():
                email = emails.objects.get(address=form['address'].value(),domain=form['domain'].value())
                email.user = r
                email.save()
                return render(request, 'items/upload_success.html')
            else:
                return render(request, 'items/upload_fail.html')
    else:
        form = email_form
        #use same template as add creditcard
    return render(request,'database/add_address.html',{'form':form})

'''
////////////////////////////////////////////////////////////////////////////
ITEMS BEGIN
-users add auction or listed price items
-creates item profile pages
-purchase listed price items
-bid on auction items
////////////////////////////////////////////////////////////////////////////
'''
@login_required(login_url='http://localhost:8000/login/')
def item_page(request,item_id):
    #get item type
    s = sells.objects.get(item_id = item_id)
    i = sale_items.objects.get(item_id__item_id=item_id)
    item_reviews = []
    sum = 0
    item_info = sale_items.objects.get(item_id=item_id)
    registered_user = RegisteredUser.objects.get(user__username=request.user.username)
    if reviews.objects.filter(item__item_id__item_id=item_id):
        item_reviews = reviews.objects.filter(item__item_id__item_id=item_id)

    if request.method=='POST':
        review = reviews_form(request.POST)
        list = add_item_list_form(request.POST,username=request.user.username)
        if s.type == 'L':
            form = purchase_amount_form(request.POST)
            if form.is_valid():
                request.session['amount'] = form['amount'].value()
                if i.amount_in_stock == 0:
                    return render(request,'items/out_of_stock.html')
                else:
                    url = 'http://localhost:8000/items/' + item_id + '/purchase/'
                    return redirect(url)

        else:
            form = place_bid_form(request.POST)
            if form.is_valid():
                request.session['bid_amount'] = form['bid_amount'].value()
                if i.current_bid is not None:
                    if i.current_bid < Decimal(form['bid_amount'].value()):
                        i.current_bid = Decimal(form['bid_amount'].value())
                        i.save()
                else:
                    i.current_bid = form['bid_amount'].value()
                    i.save()

                if bids.objects.create(bid_amount=form['bid_amount'].value(),item_bid_on=i,bidder=registered_user):
                    return render(request, 'items/upload_success.html')
                else:
                    return render(request, 'items/upload_fail.html')
        #add review
        if review.is_valid():
            print("creating review for item ",s.item_id)
            r = reviews.objects.create(stars = review['stars'].value(),
                                   description = review['description'].value(),
                                   item=i,
                                   rater=registered_user)
            if orders.objects.filter(item=i, user=registered_user) is not None:
                r.verified_purchase = True
            r.save()
            #need to refresh page for avg rating to propogate

            if item_reviews.count() is not None:
                for w in item_reviews:
                    sum += w.stars
                sum = sum / item_reviews.count()
                i.average_rating = sum
            else:
                i.average_rating = r.stars
            i.save()

            return render(request,'items/upload_success.html')

        if list.is_valid():
            add_to_list = user_list.objects.get(user = registered_user,list_name=list['list_name'].value())
            print("added item to list: ",add_to_list.list_name,i.item_id.item_id)
            add_to_list.item.add(i)
            add_to_list.save()
            return render(request,'items/upload_success.html')

    else:
        if s.type == 'L':
            form = purchase_amount_form
        else:
            form = place_bid_form
        review = reviews_form
        list = add_item_list_form(username=request.user.username)
    return render(request, 'items/item_profile.html',{'item':item_info, 'form':form,
                                                      's':s, 'review':review,'item_reviews':item_reviews,'list':list})

'''
new profile page that presents user sale items as well
'''
@login_required(login_url='http://localhost:8000/login/')
def view_user_sale_items(request,user_name):
    u = User.objects.get(username=user_name)
    registered_user = RegisteredUser.objects.get(user=u)
    registered_user.username = user_name
    user_reviews = reviews.objects.filter(ratee=registered_user)
    user_orders = orders.objects.filter(user__user__username=user_name)
    purchased = 0
    cat = ''
    suggestions = ''
    if user_orders.count() == 0:
        purchased = 0
    else:
        purchased = 1
        cat = user_orders.first().item.category
        y = random.randint(1, sale_items.objects.filter(category=cat).count())
        suggestions = sale_items.objects.filter(category=cat)[y:(y + 3)]
    sum = 0

    items = sale_items.objects.filter(item_id__user__user__username=user_name)
    if request.method=='POST':
        review = reviews_form(request.POST)
        if review.is_valid():
            print("creating review for user ", registered_user.user.username)
            user = RegisteredUser.objects.get(user__username=request.user.username)
            r = reviews.objects.create(stars=review['stars'].value(),
                                        description=review['description'].value(),
                                        rater=user)
            r.ratee.add(registered_user)
            r.save()
            # calculate user avg rating
            for i in user_reviews:
                sum += i.stars
            print(sum)
            sum = sum / user_reviews.count()
            registered_user.average_rating = sum
            registered_user.save()
    else:
        review = reviews_form
    return render(request,'database/user_profile.html',{'items':items, 'registered_user':registered_user,'review':review,'reviews':user_reviews, 'purchased':purchased, 'suggestions':suggestions})


#gets called from sell item, populates fields in sale_item table
#populates both auction items and listed items based form request.session['type']
@login_required(login_url='http://localhost:8000/login/')
def upload_auction_list_item(request):
    if request.method == "POST":
        if(request.session['type'] == 'A'):
            form = upload_auction_item_form(request.POST)
            if form.is_valid():
                seller = sells.objects.get(item_id=request.session['item_id'])
                if form.save():
                    item = sale_items.objects.get(item_name=form['item_name'].value(), description=form['description'].value())
                    item.item_id = seller
                    item.valid_auction = 1
                    item.save()
                    category = item.category
                    category.number_of_items_contained += 1
                    category.save()
                    return render(request,'items/upload_success.html')
                else:
                    return render(request,'items/upload_fail.html')
        else:
            form = upload_list_item_form(request.POST)
            if form.is_valid():
                seller = sells.objects.get(item_id=request.session['item_id'])
                if form.save():
                    item = sale_items.objects.get(item_name=form['item_name'].value(), description=form['description'].value())
                    item.item_id = seller
                    item.save()
                    print(item.item_id.item_id)
                    category = item.category
                    category.number_of_items_contained += 1
                    category.save()
                    return render(request,'items/upload_success.html')
                else:
                    return render(request,'items/upload_fail.html')

    else:
        if request.session['type'] == 'A':
            form=upload_auction_item_form()
        else:
            form=upload_list_item_form()
    return render(request,'items/upload_item.html',{'form':form})



'''
initial call for users to sell items
-determines type of item and populates fields accordingly
'''
@login_required(login_url='http://localhost:8000/login/')
def sell_item(request):
    #if request.user.is_authenticated:
    #form = sell_item(request.POST)

    if request.method == 'POST':
        #user = request.user
        form = sell_item_form(request.POST)
        if form.is_valid():
            if form.save():
                #store some vars for later
                request.session['username'] = request.user.username
                request.session['type'] = form['type'].value()
                user = User.objects.get(username=request.session['username'])
                registered_user = RegisteredUser.objects.get(user=user)
                sell_inst = sells.objects.filter(type=request.session['type']).latest('item_id')
                sell_inst.user = registered_user
                sell_inst.save()    #remember this...
                request.session['item_id'] = sell_inst.item_id
                print(sell_inst.item_id, sell_inst.user.user.username)
                return redirect('database:upload_auction_list_item')
            #return render(request,'database/create_user_info.html')

    else:
        form = sell_item_form
    return render(request,'items/upload_item.html',{'form':form})

'''
-purchase page redirected from item_profile page
-lets user choose credit card to use,ship address, and shipment date
-bidding stuff not finished yet
-still  need to update item amounts in items table if a sale occurs
'''
@login_required(login_url='http://localhost:8000/login/')
def purchase(request,item_id):
    if request.method=='POST':
        order = orders_form(request.POST,username=request.user.username)
        if order.is_valid():
            r = RegisteredUser.objects.get(user__username=request.user.username)
            #find other orders to the same place and date
            a = orders.objects.filter(ship_date = order['ship_date'].value(),
                                      ship_address=order['ship_address'].value(),
                                     user=r)
            i = sale_items.objects.get(item_id__item_id=item_id)
            o = orders.objects.create(credit_card=order['credit_card'].value(),
                                      ship_date = order['ship_date'].value(),
                                      ship_address=order['ship_address'].value())
            s = sells.objects.get(item_id=item_id)
            print(o.order_id)
            #set order info
            o.user = r
            o.item = i
            o.amount = request.session['amount']
            #set aggregate if query exists
            if a is not None:
                for k in a:
                    if k.aggregate_with is not None:
                        pass
                    else:
                        o.aggregate_with = k


            #determine if seller is user or supplier
            if s.user is not None:
                o.seller = s.user.user.username
            else:
                o.seller=s.supplier.supplier_id

            #use as bid winner page as well
            if i.listed_price is not None:
                o.item_cost = i.listed_price
            else:
                o.item_cost = i.current_bid

            #increment categories and decrement amounts
            category = i.category
            category.number_of_items_sold += int(request.session['amount'])
            i.amount_in_stock -= int(request.session['amount'])
            category.save()
            i.save()
            o.save()
            return render(request, 'items/upload_success.html')
            #else:
                #return render(request,'items/upload_fail.html')
    else:
        order = orders_form(username=request.user.username)

    return render(request,'items/purchase.html',{'form':order})


@login_required(login_url='http://localhost:8000/login/')
def view_user_list(request,user_name):
    u = RegisteredUser.objects.get(user__username=request.user.username)
    list_contents = []
    if request.method == "POST":
        lists = add_item_list_form(request.POST,username=request.user.username)
        if lists.is_valid():
            list_contents = user_list.objects.get(user = u, list_name=lists['list_name'].value())
            return render(request,'items/view_list.html',{'lists':lists, 'list_contents':list_contents})
    else:
        lists = add_item_list_form(username=request.user.username)

    return render(request,'items/view_list.html',{'lists':lists,'list_contents':list_contents})


@login_required(login_url='http://localhost:8000/login/')
def create_user_list(request,user_name):
    u = RegisteredUser.objects.get(user__username=request.user.username)
    same_name = ''
    if request.method == "POST":
        form = add_list_form(request.POST)
        if form.is_valid():
            user_lists = user_list.objects.filter(user = u)
            if user_list is not None:
                for i in user_list:
                    if i.list_name == form['item_list'].value():
                        same_name= 'Please Use a New List Name'
                        return render(request,'items/add_list.html',{'form':form, 'same_name':same_name})
            list = user_list.objects.create(list_name=form['list_name'].value(), user = u)
            list.save()
            return render(request, 'items/upload_success.html')
    else:
        form = add_list_form
    return render(request, 'items/add_list.html',{'form':form,'same_name':same_name})


#Trying to implement search


def SearchView(request):
    query1 = {}

    for i in request.META["QUERY_STRING"].split("&"):
        query1[i.split("=")[0]] = i.split("=")[1]

    search = query1["search"]
    query = sale_items.objects.filter(Q(item_name__icontains=search) |
                                              Q(description__icontains=search))


    return render(request, 'database/search_results.html', {'query':query, 'search':search})


def display_orders(request,user_name):
    o = orders.objects.filter(user__user__username=user_name)
    return render(request,'database/order_history.html',{'orders':o})

def cancel_item(request,item_id):
    item = sale_items.objects.get(item_id__item_id=item_id)
    item.amount_in_stock = 0
    item.save()
    return render(request,'items/item_canceled.html',{'item':item})

def relist_item(request,item_id):
    item = sale_items.objects.get(item_id__item_id=item_id)
    if request.method == "POST":
        if item.item_id.type == 'A':
            form = relist_auction_form(request.POST)
            if form.is_valid():
                item.amount_in_stock = form['item_amount'].value()
                item.reserve_price = form['auction_reserve'].value()
                item.valid_auction = 1
                item.auction_end_date = form['auction_end_date'].value()
                item.auction_end_time = form['auction_end_time'].value()
                item.current_bid = 0
                item.save()
                return render(request,'items/upload_success.html')
        if item.item_id.type == 'L':
            form = relist_list_form(request.POST)
            if form.is_valid():
                item.amount_in_stock = form['item_amount'].value()
                item.listed_price = form['item_price'].value()
                item.save()
                return render(request,'items/upload_success.html')
    else:
        if item.item_id.type == 'A':
            form = relist_auction_form
        else:
            form = relist_list_form
    return render(request,'items/item_relist.html',{'form':form})


