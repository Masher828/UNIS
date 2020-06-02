from django.urls import path
from . import views

app_name = 'chats'
urlpatterns = [
    path('',views.chat_home, name = "chat_home"),
    path('get_user/',views.get_users,name="get_users"),
    path('get_user_details/',views.get_user_details,name ="get_user_details"),
    path('adduser/',views.addcontact, name = "addcontact"),
    # path('create_chat_table/',view.create_chat_table,name = "create_chat_table"),
]
