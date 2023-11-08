from django.urls import path

from apps.list.views import HomePageView, my_list_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('lists/<slug:slug>/', my_list_view, name='lists'),
]
