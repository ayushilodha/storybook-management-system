


from turtle import title
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import  *
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control

# Create your views here.


def unpack():
    global filepath
    global size
    global hashtable
    size =10
    filepath = "fs1.txt"
    try:
        f = open(filepath)
        #file Exists
        f.close()
        f = open(filepath,"r")
    except FileNotFoundError:
        #File does not exist
        f=open(filepath,"w+")
        for i in range(size):
            f.write("##|##|##|##|##\n")
        f.close()
    hashtable=[]  #our hashtable is a list of lists
    for i in range(size):
        tempList = []
        hashtable.append(tempList)
    f = open(filepath,"r")
    if f.mode == 'r':
        f1=f.read()
        lines = f1.split("\n")
        count =0
        for i in lines:
            count = count+1
            c = i.split("|")
            hashtable[count-1] = c
            if count == size :
                break


def pack(hashtable):
    f = open(filepath, "w")
    count = 0
    for entry in hashtable:
        record = entry[0]+"|"+entry[1]+"|"+entry[2]+"|"+entry[3]+"|"+entry[4]+"\n" #index 0--title,index 1--author,index 2--publisher 3--year of publish, 4--genre
        f.write(record)
    f.close()

def hashvalue(title):
    key = ord(title[0])+ord(title[len(title)-1])
    print(key)
    return key

def insert(bookInfo):
    unpack()
    hashkey = hashvalue(bookInfo[0])
    if hashtable[hashkey%size][0] == bookInfo[0]:
        print("duplicate record cannot be inserted")
        return 1
    elif hashtable[hashkey%size][0] == "##" or hashtable[hashkey%size][0] == "$$":
        hashtable[hashkey%size] = bookInfo
    else:
        hashkey = hashkey+1
        count =0
        while hashtable[hashkey%size][0] != "##" and hashtable[hashkey%size][0] != "$$":
            if hashtable[hashkey%size][0] != bookInfo[0]:
                hashkey = hashkey+1
                print(count)
                count=count+1
                if count == size:
                    print("table is full")
                    return 2
            else:
                print("duplicate record cannot be inserted")
                return 1
        hashtable[hashkey%size] = bookInfo        
    pack(hashtable)
    return 0

def search(title):
    unpack()
    hashkey = hashvalue(title)
    if hashtable[hashkey%10][0] == title:
        return hashtable[hashkey%10] +[hashkey%10]
    else:
        hashkey = hashkey+1
        count =0
        while hashtable[hashkey%10][0] != title:
            hashkey = hashkey+1
            count=count+1
            if count == 10:
                return [-1]
        return hashtable[hashkey%10] +[hashkey%10]

def remove(title):
    k = search(title)
    if(len(k)==1):
        return -1 #title not present
    else:
        hashtable[k[5]][0] = "$$"
    pack(hashtable)
    return 0


def edit(bookInfo):
    unpack()
    toModify = search(bookInfo[0])
    if len(toModify)==1:
        print("Wrong title!")
        return -1
    else:
        hashtable[toModify[5]][1] = bookInfo[1]
        hashtable[toModify[5]][2] = bookInfo[2]
        hashtable[toModify[5]][3] = bookInfo[3]
        hashtable[toModify[5]][4] = bookInfo[4]
        pack(hashtable)
        return 1


def login(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username =='varsha' and password =='1234567':
                return redirect('/add/')
        return render(request,'story/login.html')


def logout(request):
    home(request)


def home(request):
    searchWord = request.POST.get('search','')
    searchWord = searchWord.upper()
    context ={}
    if(searchWord != ''):
        k = search(searchWord)
        if(len(k) == 1):
            context = {'searchWord':['Record not found']}
        else:
            send = ["Title: "+k[0]," Author: "+k[1]," Publisher: "+k[2]," Year of publish: "+k[3]," Genre: "+k[4]]
            context = {'searchWord':send}
    return render(request,'story/index.html',context)


def add(request):
    context={}
    context['k'] = -1
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            title = title.upper()
            author = form.cleaned_data['author']
            author = author.upper()
            publisher= form.cleaned_data['publisher']
            publisher = publisher.upper()
            year_of_publish= form.cleaned_data['year_of_publish']
            year_of_publish = year_of_publish.upper()
            genre= form.cleaned_data['genre']
            genre = genre.upper()
            k = insert([title,author,publisher,year_of_publish,genre])
            context['k'] = k
            form = BookForm()
            context['form'] = form
            return render(request, 'story/add.html',context)
    context['form'] = form
    print(context['k'])
    return render(request, 'story/add.html',context)

def delete(request):
    searchWord = request.POST.get('search','')
    searchWord = searchWord.upper()
    context ={}
    if(searchWord != ''):
        k = remove(searchWord)
        if(k == -1):
            context = {'searchWord':-1}
        else:
            context = {'searchWord': 1}
    return render(request, 'story/delete.html',context)

def display(request):
    unpack()
    table =[]
    for i in hashtable:
        templist =[]
        if i[0] =='$$':
            templist = ["this record is deleted","-","-","-","-"]
        else:
            templist = i
        table.append(templist)
    context = {'data':table}
    return render(request, 'story/display.html',context)


def modify(request):
    context={}
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            title = title.upper()
            author = form.cleaned_data['author']
            author = author.upper()
            publisher= form.cleaned_data['publisher']
            publisher = publisher.upper()
            year_of_publish= form.cleaned_data['year_of_publish']
            genre= form.cleaned_data['genre']
            genre = genre.upper()
            k=edit([title,author,publisher,year_of_publish,genre])
            context['k'] = k
            form = BookForm()
            context['form'] = form
            return render(request, 'story/modify.html',context)
    context = {'form':form}
    return render(request, 'story/modify.html',context)

def modify1(request):
    searchWord = request.POST.get('search','')
    searchWord = searchWord.upper()
    context ={}
    global toModify
    if(searchWord != ''):
        toModify = search(searchWord)
        if(len(toModify) == 1):
            context = {'searchWord':['Record not found']}
            context['val'] = -1
        else:
            send = ["Title: "+toModify[0]," Author: "+toModify[1]," Publisher: "+toModify[2]," Year of publish: "+toModify[3]," Genre: "+toModify[4]]
            context = {'searchWord':send}
            context['val'] = 1
    return render(request,'story/modify1.html',context)