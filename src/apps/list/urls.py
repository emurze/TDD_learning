from django.urls import path

from apps.list.views import home_page_view

app_name = 'list'

urlpatterns = [
    path('', home_page_view, name='home_page'),
]
