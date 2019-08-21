from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login_try$', views.login_try),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^upload_fav_book$', views.upload_fav_book),
    url(r'^books/(?P<id>\d+)$', views.book),
    url(r'^books/update/(?P<id>\d+)$', views.update_book),
    url(r'^books/delete/(?P<id>\d+)$' , views.delete_book),
    url(r'^books/unfavorite/(?P<id>\d+)$', views.unfavorite_book),
    url(r'^books/add_to_favorite/(?P<id>\d+)$', views.add_to_favorite),
    url(r'^user$', views.user_favorites),
]