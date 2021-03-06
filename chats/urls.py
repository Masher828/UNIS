from django.urls import path
from . import views

app_name = 'chats'
urlpatterns = [
    path('',views.chat_home, name = "chat_home"),
    path('get_user/',views.get_users,name="get_users"),
    path('get_user_details/',views.get_user_details,name ="get_user_details"),
    path('adduser/',views.addcontact, name = "addcontact"),
    path('get_friends/',views.get_friends,name = "get_friends"),
    path('get_chat_list/',views.get_chat_list,name="get_chat_list"),
    path('get_friends_chat/',views.get_friends_chat, name ="get_friends_chat"),
    path('send_message/',views.send_message, name = "send_message"),
    path('delete_message/',views.delete_message,name="delete_message"),
    path('clear_chat/',views.clear_chat,name="clear_chat"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('sendimagemsg/',views.sendimagemsg,name ="sendimagems/"),
    path('get_last_chat/',views.get_last_chat, name ="get_last_chat"),
]
