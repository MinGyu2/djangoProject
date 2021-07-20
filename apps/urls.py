from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('<int:num>/', views.mainpage_menuselect, name='mainpage_menuselect')
]