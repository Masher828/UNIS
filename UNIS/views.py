from django.shortcuts import render
import psycopg2
def home(request):
    return render(request,'index.html')

def error4o4(request, exception):
    return render(request,'error4o4.html')
