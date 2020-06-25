from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Details,Customprofilepic
from django.contrib import auth
import psycopg2
from django.http import HttpResponse, Http404
import secrets
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


class connect_DB:
    def __init__(self):
        self.connection= psycopg2.connect(user = "postgres", host="localhost",database ="unis_db",password="I*p96U#o4eID^Ubc$R*Y", port= 5433)
        self.cursor = self.connection.cursor()

    def execute(self,query,autocommit=False,returnRows=False):
        if autocommit:
            self.connection.autocommit=True
        self.cursor.execute(query)
        if returnRows == "all":
            return self.cursor.fetchall()
        elif returnRows == "one":
            return self.cursor.fetchone()

    def returnCursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()
    
    def multipleExecute(self,queries):
        for query in queries:
            self.cursor.execute(query)

    def close(self):
        self.cursor.close()
        self.connection.close()


def login(request):
    if request.method == 'POST' and request.user.is_anonymous:
            username_lowercase = request.POST['username'].lower()
            user = auth.authenticate(username = username_lowercase, password = request.POST['password'])
            if user is not None:
                auth.login(request,user)
                return redirect('chats:chat_home')

            else:
                return render(request,'accounts/signin.html',{'error':'user does not exist'})
    else:
        return render(request,'accounts/signin.html')


def logout(request):
    if request.user.is_anonymous:
        raise Http404
    else:
        auth.logout(request)
        return redirect('index')

def signup(request):
    customprofilepic_obj = Customprofilepic.objects.all()
    if request.method == 'POST' and not(request.user.is_anonymous):
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
                    try:
                        detail.Profile_pic = request.FILES['Profile_pic']
                    except:
                        try:
                            detail.Profile_pic = get_object_or_404(Customprofilepic,pk= request.POST['imgid']).custom_DP
                        except:
                            detail.Profile_pic = get_object_or_404(Customprofilepic,pk= 1).custom_DP

                    detail.status = "Available"
                    create_table_query = '''CREATE TABLE {}_contacts(contact_id INT PRIMARY KEY, last_chat VARCHAR(60), isRead VARCHAR(6), isTyping VARCHAR(6), unread_count INT, isFriend VARCHAR(5)); '''.format(lower_case_username)
                    postgres_db = connect_DB()
                    postgres_db.execute(create_table_query,autocommit=True)
                    postgres_db.close()
                    detail.save()
                    # user = auth.authenticate(username = lower_case_username, password = request.POST['password1'])
                    # auth.login(request,user)
                    return redirect('chats:chat_home')
                except Exception as error:
                    return render(request,'accounts/signup.html',{'error':error,'images':customprofilepic_obj})
        else:
            return render(request,'accounts/signup.html',{'error':'Passwords should match','images':customprofilepic_obj})
    else:

        # customprofilepic_obj = customprofilepic_obj.objects.all()
        return render(request,'accounts/signup.html',{'images':customprofilepic_obj})

def sendCode(request):
    print(request.user.is_anonymous)
    if not request.user.is_anonymous:
        raise Http404
    else:
        alphabet = string.ascii_letters + string.digits
        resetToken = ''.join(secrets.choice(alphabet) for i in range(6))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('unisnoreply.chatting@gmail.com', 'd@j6jQ7mofRdXGJ^iUoS4cX!')
        msg = MIMEMultipart()
        msg['From'] = 'unisnoreply.chatting@gmail.com'
        msg['To'] = str(request.user.email)
        msg['Subject'] = "OTP for Password Change"
        text = 'Here is your Password Reset OTP : \n'
        html = "<h1> OTP : "+ resetToken + "</h1>"
        text2 = "\nThis OTP will expire in 5 minutes.\nIgnore, if you have not requested for password change."
        part1 = MIMEText(text,'plain')
        part2 = MIMEText(html,"html")
        part3 = MIMEText(text2,"plain")
        msg.attach(part1)
        msg.attach(part2)
        msg.attach(part3)
        s.send_message(msg)
        del msg
        s.quit()
        print(resetToken)
        return HttpResponse(resetToken)
    
