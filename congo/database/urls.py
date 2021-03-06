from django.conf.urls import url
from . import views

app_name='database'
urlpatterns = [
    url(r'^$', views.index_page, name='index_page'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^u/(?P<user_name>\w+)/$',views.view_user_sale_items, name='user_profile'),
    url(r'^u/(?P<user_name>\w+)/create_user_list/$',views.create_user_list,name='create_user_list'),
    url(r'^u/(?P<user_name>\w+)/view_list/$', views.view_user_list, name='view_user_list'),
    url(r'^u/(?P<user_name>\w+)/order_history/$', views.display_orders, name='display_order'),
    url(r'^view_users/$',views.view_users,name='view_users'),
    url(r'^create_user/$', views.create_user,name='create_user'),
    #url(r'^create_user/create_user_info/$', views.create_user_info,name='create_user_info'),
    url(r'^create_user/profile/$', views.view_profile,name='view_profile'),
    url(r'^create_supplier/$', views.create_supplier, name='create_supplier'),
    url(r'^create_supplier/supplier_profile/$', views.supplier_profile, name='supplier_profile'),
    url(r'^add_credit_card/$',views.add_credit_card,name='add_credit_card'),
    url(r'^add_address/$',views.add_address,name='add_address'),
    url(r'^add_email/$',views.add_email,name='add_email'),
    #items
    url(r'^items/(?P<item_id>\w+)/$', views.item_page, name='item_page'),
    url(r'^items/(?P<item_id>\w+)/cancel/$', views.cancel_item, name='cancel_item'),
    url(r'^items/(?P<item_id>\w+)/relist/$', views.relist_item, name='relist_item'),
    url(r'^sell/$', views.sell_item, name='sell_item'),
    url(r'^sell/item_info/$', views.upload_auction_list_item, name='upload_auction_list_item'),
    url(r'^items/(?P<item_id>\w+)/purchase/$',views.purchase,name='purchase'),
    #url(r'^search_results/(?P<search>\w+)/$', views.SearchView,name='search')
    url(r'^search_results', views.SearchView),
]


