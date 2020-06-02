from django.shortcuts import render, get_object_or_404
from accounts.models import Details
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

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



def addcontact(request):
    if request.method == "POST":
        id = request.POST['id1']

        account_id1 = get_object_or_404(Details, pk=request.user.id)
        account_id2 = get_object_or_404(Details, pk=id1)
        print(account_id1.username)
        print(account_id2.username)


def chat_loggedin(request):
    details = Details()
    details
    return render(request,'chats/retreiveddata.html',{})
