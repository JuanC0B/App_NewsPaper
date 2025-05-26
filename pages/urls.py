from django.urls import path
#from django.contrib.auth.views import LogoutView
from.views import HomePageView

urlpatterns = [
    path('', HomePageView, name='home'),
    #path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
