from django.urls import path

from apps.list.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
]
