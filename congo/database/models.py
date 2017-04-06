from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class sells(models.Model):
    AUCTION = 'A'
    LISTED_PRICE = 'L'
    SALE_ITEM_CHOICES = (
        (AUCTION, 'auction_items'),
        (LISTED_PRICE, 'listed_price_items')
    )
    type = models.CharField(max_length=10, choices=SALE_ITEM_CHOICES)
    # supplier = models.ForeignKey(supplier,on_delete=models.CASCADE,null=True)
    # user = models.ForeignKey(registered_user,on_delete=models.CASCADE,null=True)
    item_id = models.AutoField(primary_key=True)


class sale_items(models.Model):
    item_id = models.OneToOneField(sells, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    url = models.CharField(max_length=100)
    place_of_origin = models.CharField(max_length=50)
    amount_in_stock = models.IntegerField()
    initial_sale_date = models.DateField()
    average_rating = models.DecimalField(max_digits=5, decimal_places=4)

    # auction items
    reserve_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    auction_end_date = models.DateField(null=True)
    auction_end_time = models.DateTimeField(null=True)
    valid_auction = models.IntegerField(default=0, null=True)

    # listed items
    listed_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)


class user_list(models.Model):
    date = models.DateField()
    number_of_purchases = models.IntegerField()
    list_name = models.CharField(max_length=30)
    # user = models.ManyToManyField(registered_user,on_delete=models.CASCADE)
    item = models.ManyToManyField(sale_items)


class emails(models.Model):
    address = models.CharField(max_length=30, primary_key=True)
    domain = models.CharField(max_length=30)


class addresses(models.Model):
    street = models.CharField(max_length=50, primary_key=True)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()


class credit_cards(models.Model):
    card_number = models.IntegerField(primary_key=True)
    expiration_date = models.DateField()
    security_code = models.IntegerField()

GENDER = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('rather not say', 'Rather not say')
)
class RegisteredUser(models.Model):
    # User model already contains username and password
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True,related_name='user_inst')
    #registered_user_id = models.AutoField(primary_key=True, default='0')
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=14, choices=GENDER, default='Male')
    phone_number = models.IntegerField(blank=True, null=True)
    annual_income = models.IntegerField(blank=True, null=True)
    average_rating = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    emails = models.ForeignKey(emails, default=0, null=True)
    addresses = models.ForeignKey(addresses, default=0, null=True)
    credit_cards = models.ForeignKey(credit_cards, default=0, null=True)
    sells = models.ForeignKey(sells, default=0, null=True)
    list = models.ForeignKey(user_list, default=0, null=True)
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
    sells = models.ForeignKey(sells, default=0, null=True)
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


class part_of_category(models.Model):
    item = models.ManyToManyField(sale_items)
    category = models.ManyToManyField(categories)


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
    item = models.ForeignKey(sale_items, on_delete=models.CASCADE)
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    order_date = models.DateField()
    order_id = models.AutoField(primary_key=True)
    seller = models.CharField(max_length=30)
    order_time = models.DateTimeField()
    amount = models.IntegerField()
    item_cost = models.DecimalField(max_digits=8, decimal_places=2)
    ship_date = models.DateField()
    credit_card = models.ForeignKey(credit_cards, on_delete=models.DO_NOTHING)
    ship_address = models.ForeignKey(addresses, on_delete=models.DO_NOTHING)
    confirmed_purchase = models.BooleanField(default=False)
    shipment_status = models.CharField(max_length=10, choices=SALE_ITEM_CHOICES)
    tracking_number = models.IntegerField()


class bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    bid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_placed = models.DateField()
    time_placed = models.DateTimeField()
    item_bid_on = models.OneToOneField(sale_items, on_delete=models.CASCADE)
    bidder = models.OneToOneField(RegisteredUser, on_delete=models.CASCADE)
