from django.contrib import admin
from .models import supplier
from .models import RegisteredUser, sells, sale_items, categories, sale_items, user_list, reviews, addresses

# Register your models here.

admin.site.register(supplier)
admin.site.register(RegisteredUser)
admin.site.register(sells)
admin.site.register(categories)
admin.site.register(sale_items)
admin.site.register(user_list)
admin.site.register(reviews)
admin.site.register(addresses)