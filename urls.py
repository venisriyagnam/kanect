from django.urls import path
from . import views
urlpatterns = [
	path('', views.signup, name = 'signup'),
	path('login/', views.login, name = 'login'),
	path('logout/', views.logout, name = 'logout'),
	path('chats/', views.chats, name = 'chats'),
	path('user-chat/', views.user_chat, name = 'user_chat'),
	path('send-message/', views.send_message, name = 'send_message')
]