from django.shortcuts import render, get_object_or_404
from accounts.models import Details
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import psycopg2
global userlist,starting
import datetime
import base64


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

@login_required()
def chat_home(request):
    if request.user.is_anonymous:
        raise Http404
    else:
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

        return render(request,'chats/chat_home.html',{'uname':uname,'status':status, 'name':name, 'date':date, 'img': img, 'email':email,'idd': idd, 'userlist' : userlist})



def get_users(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        return HttpResponse(json.dumps(userlist))
    else:
        raise Http404
    


@csrf_exempt
def get_user_details(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        details = get_object_or_404(Details,pk=request.POST['id'])
        out_data={}
        out_data['uname'] = details.user.username
        out_data['img'] = details.Profile_pic.url
        out_data['name'] = details.user.first_name + " "+ details.user.last_name
        out_data['status'] = details.status
        return HttpResponse(json.dumps(out_data))
    else:
        raise Http404

@csrf_exempt
@login_required()
def get_friends(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db = connect_DB()
        select_friends_query = '''SELECT contact_id,isFriend FROM {}_contacts;'''.format(request.user.username)
        data = postgres_db.execute(query=select_friends_query,returnRows="all")
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'fname':[], 'lname':[], 'isFriend':[]}
        for row in data:
            detail_friend_obj = get_object_or_404(Details,pk=row[0])
            friends['id'].append(row[0])
            friends['status'].append(detail_friend_obj.status)
            friends['profile_pic'].append(detail_friend_obj.Profile_pic.url)
            friends['fname'].append(detail_friend_obj.user.first_name)
            friends['lname'].append(detail_friend_obj.user.last_name)
            friends['isFriend'].append(row[1])
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
        postgres_db.close()
        return HttpResponse(json.dumps(friends))
    else:
        raise Http404


@csrf_exempt
def addcontact(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db = connect_DB()
        #id1 -> logged in user
        #id2 -> user to be added
        account_id1 = get_object_or_404(Details, pk=request.POST['id1'])
        account_id2 = get_object_or_404(Details, pk=request.POST['id2'])
        create_table_query_logged_in = '''CREATE TABLE {}( message_id  SERIAL PRIMARY KEY, sender_id INT, body VARCHAR(8005), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_data bytea, image_type VARCHAR(50)); '''.format(account_id1.user.username+"_chat_"+account_id2.user.username)
        postgres_db.execute(query=create_table_query_logged_in,autocommit=True)
        insert_contact_logged_in = '''INSERT INTO {5}_contacts (contact_id , isRead, isTyping , unread_count,isFriend) VALUES({0},{1},{2},{3},{4})'''.format(request.POST['id2'],'false','false',0,'11', account_id1.user.username)
        postgres_db.execute(query=insert_contact_logged_in,autocommit=True)
        create_table_query_other_user = '''CREATE TABLE {}(message_id  SERIAL PRIMARY KEY, sender_id INT, body VARCHAR(8005), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_data bytea, image_type VARCHAR(50)); '''.format(account_id2.user.username+"_chat_"+account_id1.user.username)
        postgres_db.execute(query=create_table_query_other_user,autocommit=True)
        insert_contact_other_user = '''INSERT INTO {5}_contacts (contact_id , isRead, isTyping , unread_count, isFriend)  VALUES({0},{1},{2},{3},{4})'''.format(request.POST['id1'],'false','false',0,'11', account_id2.user.username)
        postgres_db.execute(query=insert_contact_other_user,autocommit=True)
        postgres_db.close()
        return HttpResponse("done")
    else:
        raise Http404

@csrf_exempt
def get_chat_list(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db = connect_DB()
        logged_in_user_id = request.POST['id']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        select_friends_query = '''SELECT contact_id,isFriend FROM {}_contacts;'''.format(logged_in_user_details_object.user.username)
        data = postgres_db.execute(query=select_friends_query,returnRows="all")
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'fname':[], 'lname':[],'email': [],'uname':[],'date':[],'last_message':[], 'timestamp':[], 'isFriend':[]}
        for row in data:
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

            friends['isFriend'].append(row[1])
            last_chat_object = postgres_db.execute(query=select_last_message,returnRows="one")
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
        postgres_db.close()

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
        return HttpResponse(json.dumps(friends))
    else:
        raise Http404


@csrf_exempt
def send_message(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db = connect_DB()
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time=str(current_time)
        logged_in_user_id = request.POST['userid']
        friend_user_id = request.POST['frienduserid']
        img_status = request.POST['isimage']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        friend_details_object = get_object_or_404(Details, pk = friend_user_id)
        table_name = logged_in_user_details_object.user.username +"_chat_"+friend_details_object.user.username
        if request.POST['isimage'] == "yes":
            img = request.POST['image']
            index= img.index(",")+1
            image_type = request.POST['image'][0:index]
            img = img[index:len(img)]
            imgdata = base64.b64decode(img)
            insert_message_query = '''INSERT INTO {0} (sender_id, ts, is_image, image_data, image_type,body)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,current_time,img_status,imgdata,image_type,"null")

        else:
            message = request.POST['message']
            insert_message_query = '''INSERT INTO {0} (sender_id , body, ts, is_image,image_data,image_type)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,message,current_time,img_status,"null","null")

        postgres_db.execute("SET timezone = 'Asia/Kolkata';", autocommit=True)
        postgres_db.execute("SET CLIENT_ENCODING = 'utf8';",autocommit=True)

        cursor = postgres_db.returnCursor()
        cursor.execute(insert_message_query,data)
        postgres_db.commit()
        table_name = friend_details_object.user.username +"_chat_"+logged_in_user_details_object.user.username
        if request.POST['isimage'] == "yes":
            insert_message_query = '''INSERT INTO {0} (sender_id, ts, is_image, image_data, image_type,body)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,current_time,img_status,imgdata,image_type,"null")

        else:
            insert_message_query = '''INSERT INTO {0} (sender_id , body, ts, is_image,image_data,image_type)  VALUES(%s,%s,%s,%s,%s,%s);'''.format(table_name)
            data = (logged_in_user_id,message,current_time,img_status,"null","null")


        cursor.execute(insert_message_query,data)
        postgres_db.commit()
        postgres_db.close()
        return HttpResponse('done')
    else:
        raise Http404



@csrf_exempt
def get_friends_chat(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db = connect_DB()
        logged_in_user_id = request.POST['userid']
        friend_user_id = request.POST['friendid']
        logged_in_user_details_object = get_object_or_404(Details,pk=logged_in_user_id)
        friend_details_object = get_object_or_404(Details, pk = friend_user_id)
        table_name = logged_in_user_details_object.user.username +"_chat_"+friend_details_object.user.username
        select_message_details_query = '''SELECT message_id,sender_id,body,ts,is_image,image_data,image_type FROM {} ORDER BY ts;'''.format(table_name)
        data = postgres_db.execute(query=select_message_details_query,returnRows="all")
        friends={'len':0,'friend_id':[],'friend_name':"" ,'message':[],'friend_profile_pic':"", 'message_id':[],'is_image': [],'image_data':[],'timestamp':[]}
        for row in data:
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
        postgres_db.close()
        return HttpResponse(json.dumps(friends))
        #senderid, frndname,chat in ascending order, frndprofile, message id, is_image,imgae_url, body time date ,isread
    else:
        raise Http404
@csrf_exempt
def delete_message(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db= connect_DB()
        user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        message_id = request.POST['message_id']
        friend_details_object = get_object_or_404(Details,pk = friend_id)
        table_name = request.user.username+"_chat_"+friend_details_object.user.username
        delete_message_query = '''DELETE FROM {0} WHERE message_id = {1};'''.format(table_name,message_id)
        postgres_db.execute(delete_message_query,autocommit=True)
        postgres_db.close()
        return HttpResponse('done')
    else:
        raise Http404


@csrf_exempt
def clear_chat(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db = connect_DB()
        user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        friend_details_object = get_object_or_404(Details,pk = friend_id)
        table_name = request.user.username+"_chat_"+friend_details_object.user.username
        clear_chat_query = '''DELETE FROM {0};'''.format(table_name)
        postgres_db.execute(clear_chat_query,autocommit=True)
        postgres_db.close()
        return HttpResponse('done')
    else:
        raise Http404

@csrf_exempt
def update_profile(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
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
    else:
        raise Http404


@csrf_exempt
def get_last_chat(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        postgres_db=connect_DB()
        logged_in_user_id = request.POST['user_id']
        friend_id = request.POST['friend_id']
        logged_in_user_details_object = get_object_or_404(Details,pk = logged_in_user_id)
        friend_details_object= get_object_or_404(Details,pk = friend_id)
        select_last_message = '''SELECT body, is_image, ts from {0} WHERE ts = ( SELECT MAX(ts) FROM {0} );'''.format(str(logged_in_user_details_object.user.username)+"_chat_"+friend_details_object.user.username)
        data = postgres_db.execute(select_last_message,returnRows="one")
        if data is None:
            data_dict = {'last_message':'','timestamp':''}
        else:
            data_dict = {'last_message':data[0],'timestamp':str(data[2])}
            if data[1] == "yes":
                data_dict['last_message']= "Photo"
        return HttpResponse(json.dumps(data_dict))
    else:
        raise Http404


@csrf_exempt
def delete_friend(request):
    if request.user.is_anonymous:
        raise Http404
    elif request.method == "POST":
        # 12 means that loggedin user has unfriended the another user and 21 means that other user has unfriended logged in user it represents the status respectively
        #2 represents 0
        postgres_db = connect_DB()
        logged_in_user_id = request.POST['userid']
        friendid = request.POST['friendid']
        friendship_status = str(request.POST['friendship_status'])
        logged_in_user_details_object = get_object_or_404(Details,pk = logged_in_user_id)
        friend_details_object = get_object_or_404(Details,pk=friendid)
        select_is_friend_query = '''select isFriend from {0}_contacts where contact_id = {1} '''.format(logged_in_user_details_object.user.username,friendid)

        is_friend=postgres_db.execute(select_is_friend_query,returnRows="one")[0]
        is_friend = str(friendship_status)+is_friend[1]
        update_is_friend_query = '''UPDATE {2}_contacts SET isFriend = ({0}) where contact_id ={1} ;'''.format(is_friend,friendid,logged_in_user_details_object.user.username)
        postgres_db.execute(update_is_friend_query)

        select_is_friend_query = '''select isFriend from {0}_contacts where contact_id = {1} '''.format(friend_details_object.user.username,logged_in_user_id)
        is_friend=postgres_db.execute(select_is_friend_query,returnRows="one")[0]
        is_friend = is_friend[0]+str(friendship_status)
        update_is_friend_query = '''UPDATE {2}_contacts SET isFriend = ({0}) where contact_id ={1} ;'''.format(is_friend,logged_in_user_id,friend_details_object.user.username)
        postgres_db.execute(update_is_friend_query)
        postgres_db.commit()
        postgres_db.close()
        return HttpResponse("Chacha vidhayak hai humare")
    else:
        raise Http404
