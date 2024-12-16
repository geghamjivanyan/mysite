#
import json

#
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as _login, logout as _logout
from datetime import datetime

#
from .models import Choice, Question, PollUser, UserLog

def index(request):
    if request.user.is_authenticated:
        my_questions = Question.objects.filter(author__user=request.user).order_by("-pub_date")
        other_questions = Question.objects.exclude(author__user=request.user).order_by("-pub_date")
        context = {
            "my_questions": my_questions,
            "other_questions": other_questions,
            "user": request.user,
        }
        usr = PollUser.objects.get(user=request.user)
        log = UserLog(user=usr, action_time=datetime.now(), action='question')
        log.save()
        return render(request, "polls/index.html", context)
    else:
        return HttpResponseRedirect('/polls/login')

def detail(request, question_id):
    if request.user.is_authenticated:
        question = get_object_or_404(Question, pk=question_id)
        if question.author.user == request.user:
            return render(request, "polls/results.html", {"question": question})
        else:
            return render(request, "polls/detail.html", {"question": question})
    else:
        return HttpResponseRedirect('/polls/login')
    
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    print("POST DATA", request.POST)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    

def register(request):
    if request.method == "GET":
        return render(request, "polls/register.html", {})
    else:
        try:
            first_name = request.POST["firstname"]
            last_name = request.POST["lastname"]
            email = request.POST["email"]
            country = request.POST["country"]
            password = request.POST["password"]
            repeat_password = request.POST["repeat_password"]
        except:
            return render(request, "polls/register.html", {"error_message": "Missed Field"})        

        if password != repeat_password:
            return render(request, "polls/register.html", {"error_message": "Password not match."})        

    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name=first_name
    user.last_name = last_name
    user.save()
    
    poll_user = PollUser(user=user, country=country)
    poll_user.save()

    return  HttpResponseRedirect('/polls/login/')

def login(request):
    if request.method == "GET":
        return render(request, 'polls/login.html', {})
    else:
        try:
            email = request.POST["email"]
            password = request.POST["password"]
        except:
            return render(request, "polls/login.html", {"error_message": "Missed Field"}) 
        
    user = authenticate(username=email, password=password)
    print("USER", email, password)
    if user:
        _login(request, user)
        usr = PollUser.objects.get(user=user)
        log = UserLog(user=usr, action_time=datetime.now(), action='login')
        log.save()
        return HttpResponseRedirect('/polls/')

    else:
        return render(request, "polls/login.html", {"error_message": "Email or password is incorrect."}) 


def logout(request):
    _logout(request)
    return HttpResponseRedirect("/polls/login")


def add_question(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, "polls/add_question.html", {})
        
        else:
            user = request.user
            puser = PollUser.objects.get(user=user)
            question_text = request.POST["question"]

            q = Question(author=puser,
                    question_text=question_text, 
                    pub_date=datetime.now()
                )
            q.save()
            return HttpResponseRedirect("/polls/" + str(q.id))


    else:
        return HttpResponseRedirect("/polls/login")    
