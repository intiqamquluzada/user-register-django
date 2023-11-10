from django.urls import path
from lssn.views import *


urlpatterns = [
    path("register/", register_view, name='register'),
]