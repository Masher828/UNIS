from django.shortcuts import render, get_object_or_404
from accounts.models import Details
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import psycopg2

global userlist

@login_required()
def chat_home(request):
    print("reached")
    print(request.user)
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
        friends={'len':0,'id':[],'status':[],'profile_pic':[],'name':[]}
        for row in cursor.fetchall():
            detail_friend_obj = get_object_or_404(Details,pk=row[0])
            friends['id'].append(row[0])
            friends['status'].append(detail_friend_obj.status)
            friends['profile_pic'].append(detail_friend_obj.Profile_pic.url)
            friends['name'].append(detail_friend_obj.user.first_name + " "+ detail_friend_obj.user.last_name)
        cursor.close()
        connection.close()
        friends['len']=len(friends['id'])
        return HttpResponse(json.dumps(friends))


@csrf_exempt
@login_required()
def addcontact(request):
    if request.method == "POST":
            #id1 -> logged in user
            #id2 -> another user
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
            create_table_query_logged_in = '''CREATE TABLE {}(sender_id INT, body VARCHAR(2000), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_url_id INT, is_read VARCHAR(8)); '''.format(account_id1.user.username+"_chat_"+account_id2.user.username)
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
            create_table_query_other_user = '''CREATE TABLE {}(sender_id INT, body VARCHAR(2000), ts TIMESTAMP, align VARCHAR(10), is_image VARCHAR(6), image_url_id INT, is_read VARCHAR(8)); '''.format(account_id2.user.username+"_chat_"+account_id1.user.username)
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




def chat_loggedin(request):
    details = Details()
    return render(request,'chats/retreiveddata.html',{})

# def create_chat_table(request):
#     pass
    # if request.method == "POST":
    #     loggedin_username= get_object_or_404(Details,pk=request.POST['']
    #     # connection = psycopg2.connect(user = "postgres",
    #     #                                   password = "I*p96U#o4eID^Ubc$R*Y",
    #     #                                   host = "localhost",
    #     #                                   port = "5433",
    #     #                                   database = "unis_{}".format(request.POST['username']))
    #     # connection.autocommit = True
    #     # create_table_query = '''CREATE TABLE contacts(contact_id INT, last_chat VARCHAR(60), isRead VARCHAR(6), isTyping VARCHAR(6), unread_count INT); '''
    #     # cursor= connection.cursor()
    #     # cursor.execute(create_table_query)
    #     # connection.commit()
    #     # cursor.close()
    #     # connection.close()
    #     # detail.save()
    #     # return redirect('chats:chat_home')
