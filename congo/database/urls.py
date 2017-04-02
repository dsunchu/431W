from django.conf.urls import url
from . import views

app_name='database'
urlpatterns = [
    url(r'^$', views.index_page, name='index_page'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^u/(?P<user_name>\w+)/$',views.view_user_profile, name='user_profile'),
    url(r'^view_users/$',views.view_users,name='view_users'),
    url(r'^create_user/$', views.create_user,name='create_user'),
    #url(r'^create_user/create_user_info/$', views.create_user_info,name='create_user_info'),
    url(r'^create_user/profile/$', views.view_profile,name='view_profile'),
    url(r'^create_supplier/$', views.create_supplier, name='create_supplier'),
    url(r'^create_supplier/supplier_profile/$', views.supplier_profile, name='supplier_profile')
]
