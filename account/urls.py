from django.urls import path

from main.views import FilmsViewSet
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('v1/api/<int:id>/favorite/', FilmsViewSet.as_view({'get': 'list'})),

]