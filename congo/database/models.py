from django.db import models
from django.contrib.auth.models import User
from itertools import chain
# Create your models here.


class sells(models.Model):
    AUCTION = 'A'
    LISTED_PRICE = 'L'
    SALE_ITEM_CHOICES = (
        (AUCTION, 'Auction'),
        (LISTED_PRICE, 'List Price')
    )
    type = models.CharField(max_length=10, choices=SALE_ITEM_CHOICES)
    supplier = models.ForeignKey('supplier',on_delete=models.CASCADE,null=True,related_name='sell_supplier')
    user = models.ForeignKey('RegisteredUser',on_delete=models.CASCADE,null=True,related_name='sell_user')
    item_id = models.AutoField(primary_key=True)
    def __str__(self):
        return str(self.item_id)


class sale_items(models.Model):
    item_id = models.OneToOneField(sells, on_delete=models.CASCADE,null=True)
    item_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    place_of_origin = models.CharField(max_length=50)
    amount_in_stock = models.IntegerField()
    initial_sale_date = models.DateField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=4,null=True)
    category = models.ForeignKey('categories', null=True, blank=True, default='All')
    # auction items
    reserve_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    auction_end_date = models.DateField(null=True)
    auction_end_time = models.TimeField(null=True)
    valid_auction = models.IntegerField(default=0, null=True)
    current_bid = models.DecimalField(max_digits=8,decimal_places=2,null=True)

    # listed items
    listed_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    def __str__(self):
        return str(self.item_id)

class user_list(models.Model):
    date = models.DateField(auto_now_add=True)
    number_of_purchases = models.IntegerField(null=True)
    list_name = models.CharField(max_length=30)
    user = models.ForeignKey('RegisteredUser',null=True)
    item = models.ManyToManyField(sale_items,null=True)


class emails(models.Model):
    address = models.CharField(max_length=30, primary_key=True)
    domain = models.CharField(max_length=30)
    user = models.ForeignKey('RegisteredUser',on_delete=models.CASCADE,null=True)


class addresses(models.Model):
    street = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    user = models.ForeignKey('RegisteredUser',on_delete=models.CASCADE,null=True)


MONTH = (
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('03', '04'),
    ('05', '05'),
    ('06', '06'),
    ('07', '07'),
    ('08', '08'),
    ('09', '09'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12')
)
class credit_cards(models.Model):
    card_number = models.IntegerField(primary_key=True)
    expiration_month = models.CharField(choices=MONTH, default='01', max_length=2)
    expiration_year = models.CharField(max_length=4, default='2017')
    security_code = models.IntegerField()
    user = models.ForeignKey('RegisteredUser', on_delete=models.CASCADE, null=True)

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('rather not say', 'Rather not say')
)
class RegisteredUser(models.Model):
    # User model already contains username and password
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='user_inst')
    #registered_user_id = models.AutoField(primary_key=True, default='0')
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=14, choices=GENDER, default='Male')
    phone_number = models.IntegerField(blank=True, null=True)
    annual_income = models.IntegerField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    #emails = models.ForeignKey(emails, default=0, null=True)
    #addresses = models.ForeignKey(addresses, default=0, null=True)
    #credit_cards = models.ForeignKey(credit_cards, default=0, null=True)
    #sells = models.ForeignKey(sells, default=0, null=True)
    #list = models.ForeignKey(user_list, default=0, null=True)
    #when the user logs in allow them to set info for auction items
    auction_winner = models.ManyToManyField(sale_items,null=True)
    auction_flag = models.BooleanField(default=False)
    def set_auction_flag(self):
        if self.auction_winner.all() is not None:
            self.auction_flag = True


    def __str__(self):
        return self.name

class supplier(models.Model):
    supplier_id = models.CharField(max_length=50, primary_key=True)
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True)
    phone_number = models.IntegerField(null=True)
    category = models.CharField(max_length=30, null=True)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    #sells = models.ForeignKey(sells, default=0, null=True)
    def __str__(self):
        return self.supplier_id

class user_rating(models.Model):
    rater = models.OneToOneField(RegisteredUser, related_name='raters', on_delete=models.CASCADE)
    ratee = models.OneToOneField(RegisteredUser, related_name='ratees', on_delete=models.CASCADE)
    stars = models.IntegerField()
    item_id = models.ForeignKey(sale_items, on_delete=models.DO_NOTHING)
    verified_purchase = models.BooleanField(default=False)


class supplier_rating(models.Model):
    user_rater = models.OneToOneField(RegisteredUser, on_delete=models.DO_NOTHING)
    stars = models.IntegerField()
    item_id = models.ForeignKey(sale_items, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=500)
    verified_purchase = models.BooleanField(default=False)


class categories(models.Model):
    category_name = models.CharField(max_length=30, primary_key=True)
    parent_category = models.CharField(max_length=30)
    number_of_items_sold = models.IntegerField()
    number_of_items_contained = models.IntegerField()
    def __str__(self):
        return self.category_name


class item_rating(models.Model):
    item = models.OneToOneField(sale_items, on_delete=models.CASCADE)
    user_rater = models.ForeignKey(RegisteredUser, on_delete=models.DO_NOTHING)
    stars = models.IntegerField()
    description = models.CharField(max_length=500)
    verified_purchase = models.BooleanField(default=False)


# =============================END ITEMS============================================
# =============================ORDERS===============================================
class orders(models.Model):
    SHIPPED = 'SHIP'
    PROCESSING = 'PROCESS'
    CANCELED = 'CANCEL'
    SALE_ITEM_CHOICES = (
        (SHIPPED, 'item_shipped'),
        (PROCESSING, 'item_order_processing'),
        (CANCELED, 'item_order_canceled')
    )
    item = models.ForeignKey(sale_items, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE,null=True)
    order_date = models.DateField(auto_now_add=True)
    order_id = models.AutoField(primary_key=True)
    seller = models.CharField(max_length=30,null=True)
    order_time = models.TimeField(auto_now_add=True)
    amount = models.IntegerField(null=True)
    item_cost = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    ship_date = models.DateField(null=True)
    credit_card = models.CharField(max_length=30,null=True)
    ship_address = models.CharField(max_length=50, null=True)
    confirmed_purchase = models.BooleanField(default=False)
    shipment_status = models.CharField(max_length=10, choices=SALE_ITEM_CHOICES,null=True)
    tracking_number = models.IntegerField(null=True)
    aggregate_with = models.ForeignKey('self',null=True)

class bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_placed = models.DateField(auto_now_add=True)
    time_placed = models.TimeField(auto_now_add=True)
    item_bid_on = models.ForeignKey(sale_items, on_delete=models.CASCADE)
    bidder = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)

class reviews(models.Model):
    item = models.ForeignKey(sale_items,null=True)
    rater = models.ForeignKey(RegisteredUser,null=True,related_name='rater')
    ratee = models.ManyToManyField(RegisteredUser,null=True,related_name='user_rating')
    supplier = models.ManyToManyField(supplier,null=True)
    description = models.CharField(max_length=500)
    stars = models.DecimalField(max_digits=5,decimal_places=4,null=True)
    verified_purchase = models.BooleanField(default=False)
    #date and time fields
