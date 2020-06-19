from django.shortcuts import render, get_object_or_404
from accounts.models import Details
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import psycopg2
global userlist,starting
import datetime

db_user = "dcdh9hmuq5hbbd"
db_name = "odinofeyjfxvir"
db_port= 5432
db_host= "ec2-34-200-15-192.compute-1.amazonaws.com"
db_online_password = "d35eb0785321fb5b5788c4322f1c442d80936cbe75fa2e439835f53a556697d2"
db_offline_password =  "I*p96U#o4eID^Ubc$R*Y"
db_pass = db_online_password

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

    return render(request,'chats/chat_home.html',{'uname':uname,'status':status, 'name':name, 'date':date, 'img': img, 'email':email,'idd': idd, 'userlist' : userlist})



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
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                      database = "unis_{}".format(request.user.username))
        # connection_other_user.autocommit = True
        select_friends_query = '''SELECT contact_id,isFriend FROM contacts;'''
        cursor= connection.cursor()
        cursor.execute(select_friends_query)
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'fname':[], 'lname':[], 'isFriend':[]}
        for row in cursor.fetchall():
            detail_friend_obj = get_object_or_404(Details,pk=row[0])
            friends['id'].append(row[0])
            friends['status'].append(detail_friend_obj.status)
            friends['profile_pic'].append(detail_friend_obj.Profile_pic.url)
            friends['fname'].append(detail_friend_obj.user.first_name)
            friends['lname'].append(detail_friend_obj.user.last_name)
            friends['isFriend'].append(row[1])
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
            key_isFriend = friends['isFriend'][i]
            j = i-1
            while j >= 0 and key < friends['fname'][j] :
                    friends['fname'][j + 1] = friends['fname'][j]
                    friends['lname'][j + 1] = friends['lname'][j]
                    friends['id'][j + 1] = friends['id'][j]
                    friends['status'][j + 1] = friends['status'][j]
                    friends['profile_pic'][j + 1] = friends['profile_pic'][j]
                    friends['isFriend'][j + 1] = friends['isFriend'][j]
                    j -= 1
            friends['fname'][j + 1] = key
            friends['lname'][j + 1] = key_lname
            friends['id'][j + 1] = key_id
            friends['status'][j + 1] = key_status
            friends['isFriend'][j + 1] = key_isFriend
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
        try:
            connection_logged_in = psycopg2.connect(user = db_user,
                                          password = db_pass,
                                          host = db_host,
                                          port = db_port,
                                                  database = "unis_{}".format(account_id1.user.username))
            connection_logged_in.autocommit = True
            create_table_query_logged_in = '''CREATE TABLE {}( message_id  SERIAL PRIMARY KEY, sender_id INT, body VARCHAR(2000), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_data bytea, image_type VARCHAR(50)); '''.format(account_id1.user.username+"_chat_"+account_id2.user.username)
            cursor_logged_in= connection_logged_in.cursor()
            cursor_logged_in.execute(create_table_query_logged_in)
            insert_contact_logged_in = '''INSERT INTO contacts (contact_id , isRead, isTyping , unread_count,isFriend) VALUES({0},{1},{2},{3},{4})'''.format(request.POST['id2'],'false','false',0,'11')
            cursor_logged_in.execute(insert_contact_logged_in)
            connection_logged_in.commit()
            cursor_logged_in.close()
            connection_logged_in.close()
            connection_other_user = psycopg2.connect(user = db_user,
                                          password = db_pass,
                                          host = db_host,
                                          port = db_port,
                                                  database = "unis_{}".format(account_id2.user.username))
            connection_other_user.autocommit = True
            create_table_query_other_user = '''CREATE TABLE {}(message_id  SERIAL PRIMARY KEY, sender_id INT, body VARCHAR(2000), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_data bytea, image_type VARCHAR(50)); '''.format(account_id2.user.username+"_chat_"+account_id1.user.username)
            cursor_other_user= connection_other_user.cursor()
            cursor_other_user.execute(create_table_query_other_user)
            insert_contact_other_user = '''INSERT INTO contacts (contact_id , isRead, isTyping , unread_count, isFriend)  VALUES({0},{1},{2},{3},{4})'''.format(request.POST['id1'],'false','false',0,'11')
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
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        select_friends_query = '''SELECT contact_id,isFriend FROM contacts;'''
        cursor= connection.cursor()
        cursor.execute(select_friends_query)
        cursor1= connection.cursor()
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'fname':[], 'lname':[],'email': [],'uname':[],'date':[],'last_message':[], 'timestamp':[], 'isFriend':[]}
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
            select_last_message = '''SELECT body, is_image, ts from {0} WHERE ts = ( SELECT MAX(ts) FROM {0} );'''.format(str(request.user)+"_chat_"+detail_friend_obj.user.username)
            cursor1.execute(select_last_message)
            friends['isFriend'].append(row[1])
            last_chat_object = cursor1.fetchone()
            if not last_chat_object is  None:
                is_image = last_chat_object[1]
                msg = last_chat_object[0]
                friends['timestamp'].append(str(last_chat_object[2]))
                if is_image != 'no':
                    friends['last_message'].append('Photo')
                else:
                    friends['last_message'].append(msg)
            else:
                friends['last_message'].append("")
                friends['timestamp'].append("")



        friends['len']=len(friends['id'])
        for i in range(1, friends['len']):
            key = friends['timestamp'][i]
            key_last_message = friends['last_message'][i]
            key_email = friends['email'][i]
            key_uname = friends['uname'][i]
            key_fname = friends['fname'][i]
            key_lname = friends['lname'][i]
            key_date = friends['date'][i]
            key_id = friends['id'][i]
            key_status = friends['status'][i]
            key_isFriend = friends['isFriend'][i]
            key_profile = friends['profile_pic'][i]
            j = i-1
            while j >= 0 and key < friends['timestamp'][j] :
                    friends['fname'][j + 1] = friends['fname'][j]
                    friends['lname'][j + 1] = friends['lname'][j]
                    friends['id'][j + 1] = friends['id'][j]
                    friends['status'][j + 1] = friends['status'][j]
                    friends['profile_pic'][j + 1] = friends['profile_pic'][j]
                    friends['timestamp'][j+1]= friends['timestamp'][j]
                    friends['uname'][j + 1] = friends['uname'][j]
                    friends['last_message'][j + 1] = friends['last_message'][j]
                    friends['date'][j + 1] = friends['date'][j]
                    friends['email'][j + 1] = friends['email'][j]
                    friends['isFriend'][j + 1] = friends['isFriend'][j]
                    j -= 1
            friends['timestamp'][j+1]= key
            friends['uname'][j + 1] = key_uname
            friends['email'][j + 1] = key_email
            friends['last_message'][j + 1] = key_last_message
            friends['fname'][j + 1] = key_fname
            friends['lname'][j + 1] = key_lname
            friends['date'][j + 1] = key_date
            friends['id'][j + 1] = key_id
            friends['status'][j + 1] = key_status
            friends['isFriend'][j + 1] = key_isFriend
            friends['profile_pic'][j + 1] = key_profile
        cursor1.close()
        cursor.close()
        connection.close()
        return HttpResponse(json.dumps(friends))


@csrf_exempt
@login_required()
def send_message(request):
    if request.method == "POST":
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time=str(current_time)
        logged_in_user_id = request.POST['userid']
        friend_user_id = request.POST['frienduserid']
        img_status = request.POST['isimage']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        friend_details_object = get_object_or_404(Details, pk = friend_user_id)
        table_name = logged_in_user_details_object.user.username +"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        connection.autocommit = True
        if request.POST['isimage'] == "yes":
            img = request.POST['image']

            index= img.index(",")+1
            image_type = request.POST['image'][0:index]
            # starting = request.POST['image'][0:index]
            img = img[index:len(img)]
            imgdata = base64.b64decode(img)
            insert_message_query = '''INSERT INTO {0} (sender_id, ts, is_image, image_data, image_type,body)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,current_time,img_status,imgdata,image_type,"null")

        else:
            message = request.POST['message']
            insert_message_query = '''INSERT INTO {0} (sender_id , body, ts, is_image,image_data,image_type)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,message,current_time,img_status,"null","null")




        cursor= connection.cursor()

        cursor.execute("SET timezone = 'Asia/Kolkata';")
        cursor.execute("SET CLIENT_ENCODING = 'utf8'")
        connection.commit()

        cursor.execute(insert_message_query,data)
        connection.commit()
        cursor.close()
        connection.close()
        table_name = friend_details_object.user.username +"_chat_"+logged_in_user_details_object.user.username
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(friend_details_object.user.username))

        if request.POST['isimage'] == "yes":
            insert_message_query = '''INSERT INTO {0} (sender_id, ts, is_image, image_data, image_type,body)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,current_time,img_status,imgdata,image_type,"null")

        else:
            insert_message_query = '''INSERT INTO {0} (sender_id , body, ts, is_image,image_data,image_type)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,message,current_time,img_status,"null","null")

        cursor= connection.cursor()

        cursor.execute("SET timezone = 'Asia/Kolkata';")
        cursor.execute("SET CLIENT_ENCODING = 'utf8'")
        connection.commit()

        cursor.execute(insert_message_query,data)
        connection.commit()
        cursor.close()
        connection.close()
        return HttpResponse('done')



import base64
@csrf_exempt
@login_required()
def get_friends_chat(request):
    if request.method == "POST":
        logged_in_user_id = request.POST['userid']
        friend_user_id = request.POST['friendid']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        friend_details_object = get_object_or_404(Details, pk = friend_user_id)
        table_name = logged_in_user_details_object.user.username +"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        select_message_details_query = '''SELECT message_id,sender_id,body,ts,is_image,image_data,image_type FROM {} ORDER BY ts;'''.format(table_name)

        cursor= connection.cursor()
        cursor.execute(select_message_details_query)
        friends={'len':0,'friend_id':[],'friend_name':"" ,'message':[],'friend_profile_pic':"", 'message_id':[],'is_image': [],'image_data':[],'timestamp':[]}
        for row in cursor.fetchall():
            detail_friend_obj = get_object_or_404(Details,pk=row[1])
            friends['message_id'].append(row[0])
            friends['friend_id'].append(row[1])
            friends['message'].append(row[2])
            strr = str(base64.b64encode(row[5]))
            strr = row[6]+strr[2:len(strr)-1]
            friends['image_data'].append(strr)
            friends['is_image'].append(row[4])

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
        table_name = request.user.username+"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(request.user.username))
        delete_message_query = '''DELETE FROM {0} WHERE message_id = {1};'''.format(table_name,message_id)
        cursor= connection.cursor()
        cursor.execute(delete_message_query)
        connection.commit()
        cursor.close()
        connection.close()
        return HttpResponse('done')


import base64
@csrf_exempt
def sendimagemsg(request):
    if request.method == "POST":
        pass


@csrf_exempt
@login_required()
def clear_chat(request):
    if request.method == "POST":

        user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        friend_details_object = get_object_or_404(Details,pk = friend_id)
        table_name = request.user.username+"_chat_"+friend_details_object.user.username
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(request.user.username))
        clear_chat_query = '''DELETE FROM {0};'''.format(table_name)
        cursor= connection.cursor()
        cursor.execute(clear_chat_query)
        connection.commit()
        cursor.close()
        connection.close()
        return HttpResponse('done')

@csrf_exempt
@login_required()
def update_profile(request):

    if request.method == "POST":
        if request.POST['update'] == 'status':
            user_id= request.POST['user_id']
            user_details_object = Details.objects.get(id = user_id)
            user_details_object.status = request.POST['status']
            user_details_object.save()
        elif request.POST['update'] ==1:
            user_details_object.Profile_pic = request.POST['profile_pic']
        elif request.POST['update'] ==1:
            user_details_object.status = request.POST['status']
        elif request.POST['update'] ==1:
            user_details_object.user.set_password(request.POST['password'])

        return HttpResponse("Return")

# @csrf_exempt
# @login_required()
# def store_chat_order(request):
#     if request.method == "POST":
#         user_id = request.POST['user_id']
#         user_details_object = Details.objects.get(id= user_id)
#         order_list = request.POST['order_list'].split("_")
#         if "postgresfrnd" in order_list:
#             order_list.remove("postgresfrnd")
#         if '' in order_list:
#             order_list.remove('')
#         order_list = set(order_list)
#         user_details_object.chat_order = order_list
#         user_details_object.save()


@csrf_exempt
@login_required()
def get_last_chat(request):
    if request.method == "POST":
        logged_in_user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        logged_in_user_details_object = get_object_or_404(Details,pk = logged_in_user_id)
        friend_details_object= get_object_or_404(Details,pk = friend_id)
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))

        cursor = connection.cursor()
        select_last_message = '''SELECT body, is_image, ts from {0} WHERE ts = ( SELECT MAX(ts) FROM {0} );'''.format(str(logged_in_user_details_object.user.username)+"_chat_"+friend_details_object.user.username)
        cursor.execute(select_last_message)
        data = cursor.fetchone()
        if data is None:
            data_dict = {'last_message':'','timestamp':''}
        else:
            data_dict = {'last_message':data[0],'timestamp':str(data[2])}
            if data[1] == "yes":
                data_dict['last_message']= "Photo"
        return HttpResponse(json.dumps(data_dict))


@csrf_exempt
@login_required()
def delete_friend(request):
    if request.method == "POST":
        # 12 means that loggedin user has unfriended the another user and 21 means that other user has unfriended logged in user it represents the status respectively
        #2 represents 0
        logged_in_user_id = request.POST['userid']
        friendid = request.POST['friendid']
        friendship_status = str(request.POST['friendship_status'])
        print(friendship_status)
        logged_in_user_details_object = get_object_or_404(Details,pk = logged_in_user_id)
        friend_details_object = get_object_or_404(Details,pk=friendid)
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(logged_in_user_details_object.user.username))
        connection.autocommit = True
        cursor = connection.cursor()
        select_is_friend_query = '''select isFriend from contacts where contact_id = {} '''.format(friendid)
        cursor.execute(select_is_friend_query);
        is_friend=cursor.fetchone()[0]
        is_friend = str(friendship_status)+is_friend[1]
        update_is_friend_query = '''UPDATE contacts SET isFriend = ({0}) where contact_id ={1} ;'''.format(is_friend,friendid)
        cursor.execute(update_is_friend_query)
        connection.commit()
        cursor.close()
        connection.close()
        connection = psycopg2.connect(user = db_user,
                                      password = db_pass,
                                      host = db_host,
                                      port = db_port,
                                              database = "unis_{}".format(friend_details_object.user.username))
        connection.autocommit = True
        cursor = connection.cursor()
        select_is_friend_query = '''select isFriend from contacts where contact_id = {} '''.format(logged_in_user_id)
        cursor.execute(select_is_friend_query);
        is_friend=cursor.fetchone()[0]
        is_friend = is_friend[0]+str(friendship_status)
        update_is_friend_query = '''UPDATE contacts SET isFriend = ({0}) where contact_id ={1} ;'''.format(is_friend,logged_in_user_id)
        cursor.execute(update_is_friend_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("completed")
        return HttpResponse("Chacha vidhayak hai humare")
