from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Details
from django.contrib import auth
import psycopg2
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == 'POST':
            print(User.objects.all())
            username_lowercase = request.POST['username'].lower()
            user = auth.authenticate(username = username_lowercase, password = request.POST['password'])
            print(user)
            if user is not None:
                auth.login(request,user)
                print(user.id)
                # for obj in Details.objects.all():
                #     print(obj.user.username)
                return redirect('chats:chat_home')

            else:
                return render(request,'accounts/signin.html',{'error':'user does not exist'})
    else:
        return render(request,'accounts/signin.html')






@login_required()
def logout(request):
    auth.logout(request)
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        print("post")
        print(request.POST)
        lower_case_username = request.POST['username'].lower()
        if request.POST['password1'] == request.POST['password2']:
            print("password verified")
            user = auth.authenticate(username = lower_case_username, password = request.POST['password1'])
            if not user is None:
                return(request,'accounts/signup.html',{'error':'user already exists'})

            else:

                    print(lower_case_username)
                    user = User.objects.create_user(username=lower_case_username,first_name = request.POST['firstname'],email=request.POST['email'], last_name = request.POST['lastname'], password=request.POST['password1'])
                    detail = Details()
                    detail.user = user
                    detail.Profile_pic = request.FILES['Profile_pic']
                    print(detail.Profile_pic.url)
                    detail.status = "Available"
                    connection = psycopg2.connect(user = "postgres",
                                                      password = "I*p96U#o4eID^Ubc$R*Y",
                                                      host = "localhost",
                                                      port = "5433")
                    connection.autocommit = True
                    create_database_query = "CREATE DATABASE unis_{};".format(lower_case_username)
                    cursor= connection.cursor()
                    cursor.execute(create_database_query)
                    cursor.close()
                    connection.close()
                    connection = psycopg2.connect(user = "postgres",
                                                      password = "I*p96U#o4eID^Ubc$R*Y",
                                                      host = "localhost",
                                                      port = "5433",
                                                      database = "unis_{}".format(lower_case_username))
                    connection.autocommit = True
                    create_table_query = '''CREATE TABLE contacts(contact_id INT PRIMARY KEY, last_chat VARCHAR(60), isRead VARCHAR(6), isTyping VARCHAR(6), unread_count INT); '''
                    cursor= connection.cursor()
                    cursor.execute(create_table_query)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    detail.save()
                    return redirect('chats:chat_home')
        else:
            return(request,'accounts/signup.html',{'error':'Passwords should match'})
    else:
        return render(request,'accounts/signup.html')
