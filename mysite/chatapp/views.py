from django.shortcuts import render
from .models import ChatRoom
# Create your views here.


def index(request):
    chatrooms=ChatRoom.objects.all()
    return render(request,'chatapp/index.html',{'chatrooms':chatrooms})


def chatroom(request,slug):
    if request.method=="POST":
        
     chatroom=ChatRoom.objects.get(slug=slug)
     messages=ChatMessage.objects.filter(room=chatroom)[0:30]
     
    return render(request,'chatapp/room.html',{'chatroom':chatroom,'messages':messages})
