from django import forms
from django.forms import extras
from .models import *


class registered_user_form(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(widget=extras.SelectDateWidget(years=range(1900,2017)))
    class Meta:
        model = RegisteredUser
        fields = ['name',
                  'date_of_birth',
                  'gender',
                  'phone_number',
                  'annual_income']

'''
class user_form(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','password']
'''
class supplier_form(forms.ModelForm):

    class Meta:
        model = supplier
        fields = [
            'supplier_id',
            'company_name',
            'address',
            'phone_number',
            'category',
            'revenue']

class credit_card_form(forms.ModelForm):
    class Meta:
        model = credit_cards
        fields = ['card_number',
                  'expiration_month',
                  'expiration_year',
                  'security_code']

class address_form(forms.ModelForm):
    class Meta:
        model = addresses
        fields = ['street',
                  'city',
                  'zip_code'
                  ]

class email_form(forms.ModelForm):
    class Meta:
        model= emails
        fields = [
            'address',
            'domain'
        ]
class upload_list_item_form(forms.ModelForm):
    class Meta:
        model = sale_items
        fields = ['item_name',
                  'description',
                  'category',
                  'url',
                  'place_of_origin',
                  'amount_in_stock',
                  'initial_sale_date',
                  'listed_price']


#remember to set valid auction field
class upload_auction_item_form(forms.ModelForm):
    #image = forms.ImageField()
    class Meta:
        model = sale_items
        fields = ['item_name',
                  'description',
                  'category',
                  'url',
                  'place_of_origin',
                  'amount_in_stock',
                  'initial_sale_date',
                  'reserve_price',
                  'auction_end_date',
                  'auction_end_time']

class sell_item_form(forms.ModelForm):
    class Meta:
        model = sells
        fields = ['type']

class purchase_amount_form(forms.Form):
    amount = forms.IntegerField()


def credit_card_choices(self,username):
    credit_set = credit_cards.objects.filter(user__user__username=username)
    choices = []
    for c in credit_set:
        choices += (c.card_number,c.card_number)

    return choices

class orders_form(forms.Form):
    ship_date = forms.DateField()
    class Meta:
        model = orders
        fields = ['credit_card','ship_date','ship_address']

    #overload init so we can prepopulate creditcards/address for users
    def __init__(self,*args,**kwargs):
        #_choices_list = kwargs.pop('_choices',None)
        username = kwargs.pop('username')
        super(orders_form,self).__init__(*args,**kwargs)
        if username is not None:
           #self.fields['username'] = username
           self.fields['credit_card'] = forms.ChoiceField(label="Credit Card Numbers",
                                                   choices=[(x.card_number, x.card_number) for x in
                                                            credit_cards.objects.filter(user__user__username=username)])
           self.fields['ship_address'] = forms.ChoiceField(label="Addresses",
                                                   choices=[(x.street, x.street) for x in
                                                            addresses.objects.filter(user__user__username=username)])



    #credit_cards = forms.IntegerField(choices=credit_card_choices(username))


class place_bid_form(forms.Form):
    bid_amount = forms.DecimalField(max_digits=8,decimal_places=2)

class reviews_form(forms.Form):
    stars = forms.DecimalField(max_digits=5,decimal_places=4)
    description = forms.CharField(max_length=500)

class add_item_list_form(forms.Form):
    class Meta:
        model = user_list
        fields = ['list_name']
    def __init__(self,*args,**kwargs):
        #_choices_list = kwargs.pop('_choices',None)
        username = kwargs.pop('username')
        super(add_item_list_form,self).__init__(*args,**kwargs)
        if username is not None:
           #self.fields['username'] = username
           self.fields['list_name'] = forms.ChoiceField(label="Lists",
                                                   choices=[(x.list_name, x.list_name) for x in
                                                            user_list.objects.filter(user__user__username=username)])


class add_list_form(forms.Form):
    list_name = forms.CharField(max_length=30)
    class Meta:
        model = user_list
        fields = ['list_name']

class search_form(forms.Form):
    options = categories.objects.all()
    category = forms.ModelChoiceField(options, initial={'All':'All'}, label='')
    search = forms.CharField(max_length=100, label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Search our inventory...'}))

class relist_list_form(forms.Form):
    item_amount = forms.IntegerField()
    item_price = forms.DecimalField(max_digits=8,decimal_places=2)

class relist_auction_form(forms.Form):
    item_amount = forms.IntegerField()
    auction_reserve = forms.DecimalField(max_digits=8,decimal_places=2)
    auction_end_date = forms.DateField(help_text='YYYY-MM-DD')
    auction_end_time = forms.TimeField(help_text='24:00')
