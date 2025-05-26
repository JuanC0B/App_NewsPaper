from django.urls import path
from .views import SignUpView, user_logout

urlpatterns =[
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', user_logout, name='logout'),
]