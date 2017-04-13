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
        if i.auction_end_date is not None and i.auction_end_time is not None:
            if i.auction_end_time < datetime.datetime.now().time() and i.auction_end_date <= datetime.datetime.now().date():
                print("Auction ended ",i.item_id.item_id)
                bid = bids.objects.filter(item_bid_on=i).latest('time_placed' and 'date_placed')
                user_email = emails.objects.get(user=bid.bidder)
                if user_email is not None:
                    print("Sent Email to Winner")
                    email_url = user_email.address + '@' + user_email.domain
                    send_mail('You have won an Auction!',
                              'Please log in to confirm order details',
                              'davidsunchu@gmail.com',
                              [email_url],
                              fail_silently=False)
                #remove object from sale_items??
                #orders.objects.create(item=i,user=bid.bidder)
                #create object for now, prompt user to populate fields when login

@shared_task
def generate_weekly_sale_reports():
    #appropriate queries here###
    #havent setup sending intervals yet
    send_mail(
        'subject',
        'Body text',
        'from@email.com',
        'to@email.com',
        fail_silently=False #enable out if fails
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