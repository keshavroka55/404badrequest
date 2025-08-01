from django.shortcuts import render


def home(request):
    return render(request,'home.html')

def success(request):
    return render(request,'login_success.html')



