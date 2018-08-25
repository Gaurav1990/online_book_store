from django.conf.urls import include, url
from django.contrib import admin
from books import views

urlpatterns = [
    # Examples:
    url(r'^$', views.AllAvailableUrls.as_view()),
    url(r'^book/$', views.BookSingleAPIs.as_view()),
    url(r'^book/(?P<isbn_id>[-\w]+)/$',views.BookSingleAPIs.as_view()),
    url(r'^books/$', views.BooksListAPI.as_view()),
    url(r'^login/$', views.LoginAPI.as_view()),

    url(r'^admin/', include(admin.site.urls)),
]
