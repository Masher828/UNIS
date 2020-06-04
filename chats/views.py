from django.shortcuts import render, get_object_or_404
from accounts.models import Details
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import psycopg2
global userlist
import datetime



@login_required()
def chat_home(request):

    global userlist
    userlist={'username':[],'id':[],'len':0}
    for obj in Details.objects.all():
            if obj.user.id == request.user.id:
                status = obj.status
                uname = obj.user.username
                name = obj.user.first_name + " "+ obj.user.last_name
                date = obj.created_at
                email = obj.user.email
                img = obj.Profile_pic.url
                idd = obj.id
            else:
                userlist['username'].append(obj.user.username)
                userlist['id'].append(obj.id)
    userlist['len']= len(userlist['id'])
    # userlist[0]= len(userlist[1])

    return render(request,'chats/index.html',{'uname':uname,'status':status, 'name':name, 'date':date, 'img': img, 'email':email,'idd': idd, 'userlist' : userlist})



def get_users(request):
    return HttpResponse(json.dumps(userlist))


@csrf_exempt
def get_user_details(request):
    details = get_object_or_404(Details,pk=request.POST['id'])
    out_data={}
    out_data['uname'] = details.user.username
    out_data['img'] = details.Profile_pic.url
    out_data['name'] = details.user.first_name + " "+ details.user.last_name
    out_data['status'] = details.status
    return HttpResponse(json.dumps(out_data))

@csrf_exempt
@login_required()
def get_friends(request):
    if request.method == "POST":
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(request.user.username))
        # connection_other_user.autocommit = True
        select_friends_query = '''SELECT contact_id FROM contacts;'''
        cursor= connection.cursor()
        cursor.execute(select_friends_query)
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'fname':[], 'lname':[]}
        for row in cursor.fetchall():
            detail_friend_obj = get_object_or_404(Details,pk=row[0])
            friends['id'].append(row[0])
            friends['status'].append(detail_friend_obj.status)
            friends['profile_pic'].append(detail_friend_obj.Profile_pic.url)
            friends['fname'].append(detail_friend_obj.user.first_name)
            friends['lname'].append(detail_friend_obj.user.last_name)
        cursor.close()
        connection.close()
        friends['len']=len(friends['id'])

        # sorting friends on the basis of their first name
        for i in range(1, friends['len']):
            key = friends['fname'][i]
            key_lname = friends['lname'][i]
            key_id = friends['id'][i]
            key_status = friends['status'][i]
            key_profile = friends['profile_pic'][i]
            j = i-1
            while j >= 0 and key < friends['fname'][j] :
                    friends['fname'][j + 1] = friends['fname'][j]
                    friends['lname'][j + 1] = friends['lname'][j]
                    friends['id'][j + 1] = friends['id'][j]
                    friends['status'][j + 1] = friends['status'][j]
                    friends['profile_pic'][j + 1] = friends['profile_pic'][j]
                    j -= 1
            friends['fname'][j + 1] = key
            friends['lname'][j + 1] = key_lname
            friends['id'][j + 1] = key_id
            friends['status'][j + 1] = key_status
            friends['profile_pic'][j + 1] = key_profile
        return HttpResponse(json.dumps(friends))


@csrf_exempt
@login_required()
def addcontact(request):
    if request.method == "POST":
        #id1 -> logged in user
        #id2 -> user to be added
        account_id1 = get_object_or_404(Details, pk=request.POST['id1'])
        account_id2 = get_object_or_404(Details, pk=request.POST['id2'])
        print(account_id1.user.username)
        print(account_id2.user.username)
        try:
            connection_logged_in = psycopg2.connect(user = "postgres",
                                                  password = "I*p96U#o4eID^Ubc$R*Y",
                                                  host = "localhost",
                                                  port = "5433",
                                                  database = "unis_{}".format(account_id1.user.username))
            connection_logged_in.autocommit = True
            create_table_query_logged_in = '''CREATE TABLE {}( message_id  SERIAL PRIMARY KEY, sender_id INT, body VARCHAR(2000), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_url_id INT, is_read VARCHAR(8)); '''.format(account_id1.user.username+"_chat_"+account_id2.user.username)
            cursor_logged_in= connection_logged_in.cursor()
            cursor_logged_in.execute(create_table_query_logged_in)
            insert_contact_logged_in = '''INSERT INTO contacts (contact_id , isRead, isTyping , unread_count) VALUES({0},{1},{2},{3})'''.format(request.POST['id2'],'false','false',0)
            cursor_logged_in.execute(insert_contact_logged_in)
            connection_logged_in.commit()
            cursor_logged_in.close()
            connection_logged_in.close()
            connection_other_user = psycopg2.connect(user = "postgres",
                                                  password = "I*p96U#o4eID^Ubc$R*Y",
                                                  host = "localhost",
                                                  port = "5433",
                                                  database = "unis_{}".format(account_id2.user.username))
            connection_other_user.autocommit = True
            create_table_query_other_user = '''CREATE TABLE {}(message_id  SERIAL PRIMARY KEY, sender_id INT, body VARCHAR(2000), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_url_id INT, is_read VARCHAR(8)); '''.format(account_id2.user.username+"_chat_"+account_id1.user.username)
            cursor_other_user= connection_other_user.cursor()
            cursor_other_user.execute(create_table_query_other_user)
            insert_contact_other_user = '''INSERT INTO contacts (contact_id , isRead, isTyping , unread_count)  VALUES({0},{1},{2},{3})'''.format(request.POST['id1'],'false','false',0)
            cursor_other_user.execute(insert_contact_other_user)
            connection_other_user.commit()
            cursor_other_user.close()
            connection_other_user.close()

            return HttpResponse("done")
        except Exception as error :
            return HttpResponse(error)
    else:
        return HttpResponse("hi") #Return page not found error

@csrf_exempt
@login_required()
def get_chat_list(request):
    if request.method == "POST":
        logged_in_user_id = request.POST['id']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        select_friends_query = '''SELECT contact_id FROM contacts;'''
        cursor= connection.cursor()
        cursor.execute(select_friends_query)
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'fname':[], 'lname':[],'email': [],'uname':[],'date':[]}
        for row in cursor.fetchall():
            detail_friend_obj = get_object_or_404(Details,pk=row[0])
            friends['id'].append(row[0])
            friends['status'].append(detail_friend_obj.status)
            friends['profile_pic'].append(detail_friend_obj.Profile_pic.url)
            friends['fname'].append(detail_friend_obj.user.first_name)
            friends['lname'].append(detail_friend_obj.user.last_name)
            friends['email'].append(detail_friend_obj.user.email)
            friends['uname'].append(detail_friend_obj.user.username)
            friends['date'].append(str(detail_friend_obj.created_at))


        friends['len']=len(friends['id'])
        cursor.close()
        connection.close()
        return HttpResponse(json.dumps(friends))


@csrf_exempt
@login_required()
def send_message(request):
    if request.method == "POST":

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(current_time)
        current_time=str(current_time)
        logged_in_user_id = request.POST['userid']

        friend_user_id = request.POST['frienduserid']
        message = request.POST['message']


        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        friend_details_object = get_object_or_404(Details, pk = friend_user_id)
        table_name = logged_in_user_details_object.user.username +"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        connection.autocommit = True

        insert_message_query = '''INSERT INTO {0} (sender_id , body, ts, is_image, image_url_id, is_read)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
        data = (logged_in_user_id,message,current_time,'false','-1','false')
        cursor= connection.cursor()

        cursor.execute("SET timezone = 'Asia/Kolkata';")
        cursor.execute("SET CLIENT_ENCODING = 'utf8'")
        connection.commit()

        cursor.execute(insert_message_query,data)
        connection.commit()
        cursor.close()
        connection.close()
        table_name = friend_details_object.user.username +"_chat_"+logged_in_user_details_object.user.username
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(friend_details_object.user.username))
        insert_message_query = '''INSERT INTO {0} (sender_id , body, ts, is_image, image_url_id, is_read)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
        data = (logged_in_user_id,message,current_time,'false','-1','false')
        cursor= connection.cursor()

        cursor.execute("SET timezone = 'Asia/Kolkata';")
        cursor.execute("SET CLIENT_ENCODING = 'utf8'")
        connection.commit()

        cursor.execute(insert_message_query,data)
        connection.commit()
        cursor.close()
        connection.close()
        return HttpResponse('done')




@csrf_exempt
@login_required()
def get_friends_chat(request):
    if request.method == "POST":
        logged_in_user_id = request.POST['userid']
        friend_user_id = request.POST['friendid']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        friend_details_object = get_object_or_404(Details, pk = friend_user_id)
        table_name = logged_in_user_details_object.user.username +"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        select_message_details_query = '''SELECT message_id,sender_id,body,ts,is_image,image_url_id,is_read FROM {} ORDER BY ts;'''.format(table_name)

        cursor= connection.cursor()
        cursor.execute(select_message_details_query)
        friends={'len':0,'friend_id':[],'friend_name':"" ,'message':[],'friend_profile_pic':"", 'message_id':[],'is_image': [],'image_url_id':[],'timestamp':[],'is_read':[]}
        for row in cursor.fetchall():
            detail_friend_obj = get_object_or_404(Details,pk=row[1])
            friends['message_id'].append(row[0])
            friends['friend_id'].append(row[1])
            friends['message'].append(row[2])
            friends['image_url_id'].append(row[5])

            friends['is_image'].append(row[4])
            friends['is_read'].append(row[6])
            friends['timestamp'].append(str(row[3]))
        detail_friend_obj = get_object_or_404(Details,pk=friend_user_id)
        friends['friend_name'] = detail_friend_obj.user.first_name + " "+ detail_friend_obj.user.last_name
        friends['friend_profile_pic'] = detail_friend_obj.Profile_pic.url
        friends['len'] = len(friends['message_id'])
        cursor.close()
        connection.close()
        return HttpResponse(json.dumps(friends))
        #senderid, frndname,chat in ascending order, frndprofile, message id, is_image,imgae_url, body time date ,isread

@csrf_exempt
@login_required()
def delete_message(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        message_id = request.POST['message_id']
        friend_details_object = get_object_or_404(Details,pk = friend_id)
        table_name = request.username+"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(request.username))
        delete_message_query = '''DELETE FROM {0} WHERE message_id = {1};'''.format(table_name,message_id)
        cursor= connection.cursor()
        cursor.execute(delete_message_query)
        cursor.close()
        connection.close()
        return HttpResponse('done')



@csrf_exempt
@login_required()
def clear_chat(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        message_id = request.POST['message_id']
        friend_details_object = get_object_or_404(Details,pk = friend_id)
        table_name = request.username+"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = "postgres",
                                              password = "I*p96U#o4eID^Ubc$R*Y",
                                              host = "localhost",
                                              port = "5433",
                                              database = "unis_{}".format(request.username))
        clear_chat_query = '''DELETE FROM {0};'''.format(table_name)
        cursor= connection.cursor()
        cursor.execute(clear_chat_query)
        cursor.close()
        connection.close()
        return HttpResponse('done')

@csrf_exempt
@login_required()
def update_profile(request):
    name,status ,profilepic,password
    if request.method == "POST":
        user_id= request.POST['user_id']
        user_details_object = get_object_or_404(Details,pk=user_id)
        if request.POST['username_status'] ==1:
            user_details_object.user.username = request.POST['username']
        if request.POST['profile_pic_status'] ==1:
            user_details_object.Profile_pic = request.POST['profile_pic']
        if request.POST['status_status'] ==1:
            user_details_object.status = request.POST['status']
        if request.POST['password_status'] ==1:
            user_details_object.user.set_password(request.POST['password'])

        return HttpResponse("Return")
