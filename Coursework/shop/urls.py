from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^basket/$', views.basket_view, name='basket'),
    url(r'^basket/add$', views.add_item, name='basket_add'),
    url(r'^basket/remove$', views.remove_item, name='basket_remove'),
    url(r'^basket/minus$', views.minus_item, name='basket_minus'),
    url(r'^basket/checkout/$', views.checkout, name='checkout'),
    url(r'^search/$', views.search, name='search'),

]
