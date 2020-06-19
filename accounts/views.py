from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Details,Customprofilepic
from django.contrib import auth
import psycopg2
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.
db_name = "dcdh9hmuq5hbbd"
db_user = "odinofeyjfxvir"
db_port= 5432
db_host= "ec2-34-200-15-192.compute-1.amazonaws.com"
db_online_password = "d35eb0785321fb5b5788c4322f1c442d80936cbe75fa2e439835f53a556697d2"
db_offline_password =  "I*p96U#o4eID^Ubc$R*Y"
db_pass = db_online_password
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
    customprofilepic_obj = Customprofilepic.objects.all()
    if request.method == 'POST':
        lower_case_username = request.POST['username'].lower()

        if request.POST['password1'] == request.POST['password2']:
            user = auth.authenticate(username = lower_case_username, password = request.POST['password1'])
            if not user is None:
                return render(request,'accounts/signup.html',{'error':'user already exists','images':customprofilepic_obj})

            else:
                try:
                    user = User.objects.create_user(username=lower_case_username,first_name = request.POST['firstname'],email=request.POST['email'], last_name = request.POST['lastname'], password=request.POST['password1'])
                    detail = Details()
                    detail.user = user
                    print(request.POST)
                    try:
                        detail.Profile_pic = request.FILES['Profile_pic']
                    except:
                        try:
                            detail.Profile_pic = get_object_or_404(Customprofilepic,pk= request.POST['imgid']).custom_DP
                        except:
                            detail.Profile_pic = get_object_or_404(Customprofilepic,pk= 1).custom_DP

                    detail.status = "Available"
                    print("lastr")
                    connection = psycopg2.connect(user = db_user,
                                                  password = db_pass,
                                                  host = db_host,
                                                  port = db_port)
                    connection.autocommit = True
                    create_database_query = "CREATE DATABASE unis_{};".format(lower_case_username)
                    cursor= connection.cursor()
                    print("lastr")
                    cursor.execute(create_database_query)
                    print("lastr")
                    cursor.close()
                    connection.close()
                    print("lastr")
                    connection = psycopg2.connect(user = db_user,
                                                  password = db_pass,
                                                  host = db_host,
                                                  port = db_port,
                                                      database = "unis_{}".format(lower_case_username))
                    connection.autocommit = True
                    create_table_query = '''CREATE TABLE contacts(contact_id INT PRIMARY KEY, last_chat VARCHAR(60), isRead VARCHAR(6), isTyping VARCHAR(6), unread_count INT, isFriend VARCHAR(5)); '''
                    cursor= connection.cursor()
                    print("lastr")
                    cursor.execute(create_table_query)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    detail.save()
                    print("lastr")
                    return redirect('chats:chat_home')
                except Exception as error:
                    return render(request,'accounts/signup.html',{'error':error,'images':customprofilepic_obj})
        else:
            return render(request,'accounts/signup.html',{'error':'Passwords should match','images':customprofilepic_obj})
    else:

        # customprofilepic_obj = customprofilepic_obj.objects.all()
        return render(request,'accounts/signup.html',{'images':customprofilepic_obj})
