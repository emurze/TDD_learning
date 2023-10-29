from django.urls import path

from apps.list.views import todo_page_view

app_name = 'list'

urlpatterns = [
    path('', todo_page_view, name='todo')
]
