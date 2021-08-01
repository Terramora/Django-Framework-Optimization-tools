from django.urls import path

from users.views import login, registrations, logout, profile, verify

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registrations/', registrations, name='registrations'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify')
]
