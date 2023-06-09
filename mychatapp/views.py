from cgi import print_arguments
from django.shortcuts import render, redirect
from .models import ChatMessage, Profile, Friend
from .forms import ChatMessageForm
from django.http import JsonResponse
import json
import pyttsx3
import os

'''
from .text_to_speech import convert_text_to_speech
def process_chat_message(request):
    # Process the chat message
    message = "Hello, how are you?"

    # Convert the message to speech
    convert_text_to_speech(message)
    '''
# Create your views here.
engine = pyttsx3.init()
def index(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        #Convert the message to speech
        engine.say(message)
        engine.runAndWait()
        # Save the chat message to the database
        ChatMessage.objects.create(message=message)
        return redirect('index')
        messages = ChatMessage.objects.all().order_by('-timestamp')[:50]
    user = request.user.profile
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, "mychatapp/index.html", context)


def detail(request,pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
    rec_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user":user, 
               "profile":profile, "chats": chats, "num": rec_chats.count()}
    return render(request, "mychatapp/detail.html", context)

def sentMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False )
    print(new_chat)

    return JsonResponse(new_chat_message.body, safe=False)

def receivedMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)





