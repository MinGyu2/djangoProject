from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('<int:num>/', views.mainpage_menuselect, name='mainpage_menuselect'),
    path('signup/', views.user_sign, name='user_sign'),
    path('delete/', views.user_del, name='user_del'),
    path('onesearch/', views.one_search_user_id, name='user_one_search'),
    path('allsearch/', views.all_search_user_id, name='user_all_search'),
]