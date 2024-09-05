from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room,Topic
from .forms import RoomForm
# Create your views here.

# rooms=[
#     {'id':1,'name':"room1"},
#     {'id':2,'name':"room2"},
#     {'id':3,'name':"room3"}  
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists")

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)    
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")
    context={'page':page}
    return render(request,'onk/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = UserCreationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'an error occured')

    return render(request,'onk/login_register.html',{'form':form})

def home(request):
    # return HttpResponse("monke")
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |
                              Q(name__icontains=q) |
                              Q(description__icontains=q)
                              )
    
    room_count =rooms.count()


    topics =Topic.objects.all()
    context ={'rooms':rooms, 'topics':topics,'room_count':room_count}
    return render(request,'onk/home.html', context)

def room(request,pk):
    # return HttpResponse("shmonke")
    # room=None
    # for i in rooms:
    #     if i['id']==int(pk):
    #         room = i
    rooms=Room.objects.get(id=pk) 
    messages = room.message_set.all()
    context={'room':room,'messages':messages}        

    return render(request,'onk/room.html',context) 


@login_required(login_url='loginPage')
def loginpg(request):
    form=RoomForm()
    if request.method == 'POST':
        form =RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


    context={'form':form}
    return render(request,"onk/room_form.html",context)

@login_required(login_url='loginPage')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user !=room.host:
        return HttpResponse('you are not allowed ')


    if request.method =='POST':
        form= RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'onk/room_form.html',context)

@login_required(login_url='loginPage')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user !=room.host:
        return HttpResponse('you are not allowed ')

    if request.method =='POST':
        room.delete()
        return redirect('home')
    
    return render(request,'onk/delete.html',{'obj':room})