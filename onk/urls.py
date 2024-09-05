from django.urls import path
from . import views

urlpatterns =[
    path('loginPage/',views.loginPage,name="loginPage"),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name="register"),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('login/',views.loginpg,name="login"),
    path('updateRoom/<str:pk>/',views.updateRoom,name="updateRoom"),
    path('deleteRoom/<str:pk>/',views.deleteRoom,name="deleteRoom")
]