from django.urls import path
from . import views

urlpatterns = [
    path('mail/',views.Dber_mail,name = 'dber_mail'),
    path('staffmail/',views.staff_mail,name = 'staff_mail'),

    path('home/',views.HomePage,name = 'home-page'),
    path('',views.register,name = 'dber-register'),
    path('update/',views.profile_update,name = 'profile_update'),
    path('login/',views.login_view,name = 'dber-login'),
    path('logout/',views.logout_view,name = 'dber-logout'),
    path('upload/',views.upload_excel,name = 'upload_excel'),
    path('ajax', views.load_cities, name='ajax_load_cities'),
    path('userlist/', views.Dber_list.as_view(), name='user-list'),
    path('userdetail/<int:pk>/', views.Dber_detail.as_view(), name='user-detail'),
]
