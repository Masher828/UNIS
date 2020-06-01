from django.shortcuts import render
from accounts.models import Details
from django.http import HttpResponse
# Create your views here.
def chat_home(request):
    
    status = Details.objects.all()[0].status
    uname = request.user.username
    name = request.user.first_name + " "+ request.user.last_name
    date = Details.objects.all()[0].created_at
    email = request.user.email
    img = Details.objects.all()[0].Profile_pic.url
    return render(request,'chats/index.html',{'uname':uname,'status':status, 'name':name, 'date':date, 'img': img, 'email':email})




#
def chat_loggedin(request):
    details = Details()
    details
    return render(request,'chats/retreiveddata.html',{})
