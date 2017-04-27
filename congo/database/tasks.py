from __future__ import absolute_import
from celery import shared_task
from .models import *
import datetime
from django.core.mail import send_mail
'''
pip install django-celery
pip install django-celery-beat
TERM 1: python manage.py celeryd --verbosity=2 --loglevel=debug
TERM 2: python manage.py celerybeat
TERM 3: python -m smtpd -n -c DebuggingServer localhost:1025 // to receive email on local before we set up read
'''
@shared_task
def auction_manager():
    print("working?")
    auction_items = sale_items.objects.filter(item_id__type='A')
    for i in auction_items:
        print(i.item_name)
        #guard for comparison
        if i.auction_end_date is not None and i.auction_end_time is not None:
            print(i.auction_end_date, i.auction_end_time, datetime.datetime.now().time(), datetime.date.today())
            if i.auction_end_date <= datetime.date.today():
                if i.auction_end_time < datetime.datetime.now().time() or i.auction_end_date < datetime.date.today():
                    print("Auction ended ",i.item_id.item_id)
                    bid = bids.objects.filter(item_bid_on=i).latest('time_placed')
                    user_email = emails.objects.get(user=bid.bidder)
                    if i.reserve_price < i.current_bid:
                        #set auction winner to notify at home
                        #get user set auction winner
                        user = bid.bidder
                        user.auction_winner.add(i)
                        user.set_auction_flag()
                        user.save()
                        print("winner ", user.user.username)
                        if user_email is not None:
                            print("Sent Email to Winner")
                            email_url = user_email.address + '@' + user_email.domain
                            send_mail('You have won an Auction!',
                                      'Please log in to confirm order details',
                                      'davidsunchu@gmail.com',
                                      [email_url],
                                      fail_silently=False)
            #else:
                #remove from items
                #sale_items.objects.get(item_id=i.item_id).delete()


@shared_task
def generate_weekly_sale_reports():
    #appropriate queries here###
    #havent setup sending intervals yet
    query = categories.objects.all()
    body_text = ''
    for i in query:
        body_text += 'CATEGORY NAME: '+ i.category_name + ' SALES: ' + i.number_of_items_sold + ' TOTAL ITEMS: ' + i.number_of_items_contained + '\n'

    send_mail(
        'subject',
        body_text,
        'from@email.com',
        'to@email.com',
        fail_silently=False #enable out if fails
    )

@shared_task
def generate_telemarket_reports():
    user_query = RegisteredUser.objects.all()
    body_text = ''
    for i in user_query:
        address = addresses.objects.filter(user=i)
        email = emails.objects.filter(user=i)
        body_text += 'user: ' + i.name + '\n'
        body_text += 'phone: ' + i.phone_number + '\n'
        body_text += 'age: ' + i.age + '\n'
        body_text += 'gender: ' + i.gender + '\n'
        body_text += 'annual income: ' + i.annual_income + '\n'
        for w in addresses:
            body_text += 'address: '+w.street+' '+w.city+' '+w.zip_code+'\n'
        for k in email:
            body_text += 'email: ' + k.address + '@' + k.domain + '\n'
    send_mail(
        'subject',
        body_text,
        'from@email.com',
        'to@email.com',
        fail_silently=False  # enable out if fails
    )


@shared_task
def add(x, y):
    print("helloworld in add from tasks.py")
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)