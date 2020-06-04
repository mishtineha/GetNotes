from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User
from cloneapp.forms import LoginForm,SigninForm, Video_Upload_form
from django .template import loader
from django.views.generic.base import View,HttpResponseRedirect
from cloneapp.views import *
from cloneapp.models import Videos , Comment , Notification, recently_viewed , Message ,Viewed_user ,Preferences , liked_video, link
from django.views.decorators.csrf import csrf_exempt
from cloneapp.models import Message
import cv2
from cloneapp.opencv import getFrame
import os
from mutagen.mp4 import MP4
from PyPDF2 import PdfFileReader
import fitz


class Addlink(View):
    def get(self,request):
        unseen_count = 0
        is_superuser = False
        if request.user.is_superuser:
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            is_superuser = True
        template = loader.get_template('html_ki_file/addlink.html')
        link_list = link.objects.all()
        context = {'links':link_list,'length':len(link_list),'is_superuser':is_superuser,'unseen_count':unseen_count}
        return HttpResponse(template.render(context,request))
    def post(self,request):
        unseen_count = 0
        is_superuser = False
        if request.user.is_superuser:
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            is_superuser = True
        l = link(link = request.POST['addlink'])
        l.save()
        link_list = link.objects.all()
        template = loader.get_template('html_ki_file/addlink.html')
        context = {'links':link_list,'length':len(link_list),'is_superuser':is_superuser,'unseen_count':unseen_count}
        return HttpResponse(template.render(context,request))
"""

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        return number_of_pages
"""

def start(request):
    logout(request)
    template = loader.get_template('html_ki_file/start.html')
    videos = Videos.objects.all()
    context = {'videos':'videos'}
    return HttpResponse(template.render(context,request))
    
    
def viewuser(request):
    #logout(request)
    #form = LoginForm()
    template = loader.get_template('html_ki_file/login2.html')
    context = {'is_alert':False}
    return HttpResponse(template.render(context,request))


def signin(request):
    #logout(request)
    
    form = SigninForm()
    template = loader.get_template('html_ki_file/signup.html')
    context = {'form':form,'is_alert':False}
    return HttpResponse(template.render(context,request))

class First(View):
    def get(self,request):
        if request.user.is_authenticated:
            return HttpResponse("authenticated")
        else:
            return HttpResponse("<h1> not authenticated </h1>")
        
    def post(self,request):
        form = SigninForm(request.POST)
        if form.is_valid():
            form1 = form.save()
            user = User.objects.last()
            login(request,user)
            return HttpResponseRedirect("../login/")
        else:
            form = SigninForm()
            template = loader.get_template('html_ki_file/signup.html')
            context = {'form':form,'is_alert':True}
            return HttpResponse(template.render(context,request))
        
class Home(View):
    def get(self,request):
        if request.user.is_authenticated:
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            template = loader.get_template('html_ki_file/testvideo.html')
            video = Videos.objects.all()
            context = {'video':video,'unseen_count':unseen_count} 
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
    def post(self,request):
        
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            template = loader.get_template('html_ki_file/testvideo.html')
            video = Videos.objects.all()
            context = {'video':video,'unseen_count':unseen_count}
            return HttpResponse(template.render(context,request))
        else:
            template = loader.get_template('html_ki_file/login2.html')
            context = {'is_alert':True}
            return HttpResponse(template.render(context,request))
            #return HttpResponse("username or password doesnot match")
class Showmsg(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser:
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            len_msg = Message.objects.filter(to = request.user).count()
            unseen_msg = Message.objects.filter(to = request.user,seen = False)
            seen_msg = Message.objects.filter(to = request.user,seen = True)
            index = len(seen_msg)
            seen = seen_msg[0:index]
            context = {'unseen_msg':unseen_msg,'seen_msg':seen,'len_msg':len_msg,'unseen_count':unseen_count}
            for msg in unseen_msg:
                msg.seen = True
                msg.save()
            template = loader.get_template('html_ki_file/showmsg.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("Login first")
        
            
class Getvideos(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {'show':False,'nodata':'nodatata','is_video':True}
            template = loader.get_template('html_ki_file/getvideo.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
class Getpdf(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {'npdata':'nodata'}
            template = loader.get_template('html_ki_file/getpdf.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
class Videoupload(View):
    def get(self,request):
        unseen = Message.objects.filter(to = request.user ,seen = False)
        unseen_count = unseen.count()
        form = Video_Upload_form()
        if request.user.is_authenticated and request.user.is_superuser:
            
            
            context = {'form':form,'unseen_count':unseen_count,'alert':False,'uploaded':False}
            template = loader.get_template('html_ki_file/videoupload.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
    def post(self,request):
        unseen = Message.objects.filter(to = request.user ,seen = False)
        unseen_count = unseen.count()
        form = Video_Upload_form(request.POST,request.FILES)
        if form.is_valid():
            if str(form.cleaned_data['videofile'])[-4::1] != ".mp4" and str(form.cleaned_data['videofile'])[-4::1] != ".pdf":
                unseen = Message.objects.filter(to = request.user ,seen = False)
                unseen_count = unseen.count()
                form = Video_Upload_form()
                context = {'form':form,'unseen_count':unseen_count,'alert':True,'uploaded':False}
                template = loader.get_template('html_ki_file/videoupload.html')
                return HttpResponse(template.render(context,request))
            size = 0
            if str(form.cleaned_data['videofile'])[-4::1] == ".mp4":
                audio = MP4(form.cleaned_data['videofile'])
                size = (audio.info.length)/60
            video = Videos(title = request.POST['title'].title(),description = request.POST['description'].title(),videofile=form.cleaned_data['videofile'],user = request.user,user_viewed = 0,size = size)
            video.save()
            video = Videos.objects.last()
            if str(form.cleaned_data['videofile'])[-4::1] == ".pdf":
                #path = "media/" + str(video.videofile)
                pdf_document = "media/" + str(video.videofile)
                doc = fitz.open(pdf_document)
                num_page = doc.pageCount
                size = num_page
                """
                with open(path, 'rb') as f:
                    pdf = PdfFileReader(f)
                    information = pdf.getDocumentInfo()
                    number_of_pages = pdf.getNumPages()
                    size = number_of_pages
                """
            video.size = size
            video.save()
            video = Videos.objects.last()
                
            #video = Videos.objects.last()
            
            getFrame(2,video.id,str(video.videofile))
            pref_teacher = Preferences.objects.filter(pref = video.user) 
            pref = Preferences.objects.filter(pref = video.title)
            pref2 = []
            prefs = Preferences.objects.all()
            for p in prefs:
                if p in pref:
                    pass
                else:
                    st = video.title
                    list_of_st = st.split()
                    for l in list_of_st:
                        if l == p.pref:
                            pref2.append(p)
            pref2.extend(pref)
            if len(pref2)!= 0:
                for p in pref2:
                    vid = video
                    mes = "new upload on the title " + p.pref
                    Notify = Notification(video = vid,msg = mes,user = p.user )
                    Notify.save()
            if len(pref_teacher)!= 0:
                for p in pref_teacher:
                    vid = video
                    mes = "new upload from teacher " + p.pref
                    Notify = Notification(video = vid,msg = mes,user = p.user )
                    Notify.save()
                 
                        
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            form = Video_Upload_form()
            videos = Videos.objects.filter(user = request.user)
            context = {'form':form,'unseen_count':unseen_count,'alert':False,'uploaded':True}
            template = loader.get_template('html_ki_file/videoupload.html')
            return HttpResponse(template.render(context,request))
        else:
            template = loader.get_template('html_ki_file/videoupload.html')
            context = {'form':form,'unseen_count':unseen_count,'alert':False,'uploaded':True}
            return HttpResponse("enter valid data<br>"+template.render(context,request))
class Recently1(View):
    def get(self,request):
        if request.user.is_authenticated:
            context = {'nodata':'nodata','is_recent':True}
            template = loader.get_template('html_ki_file/recently1.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
    
def viewuser2(request):
    logout(request)
    form = LoginForm()
    template = loader.get_template('html_ki_file/login.html')
    context = {'form':form,'is_alert':False}
    return HttpResponse(template.render(context,request))
class Login(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser == False:
            pers = Preferences.objects.filter(user = request.user)
            unseen_count = Notification.objects.filter(seen = False,user = request.user).count()
            notify = Notification.objects.filter(user = request.user)
            unseen_notify = Notification.objects.filter(seen = False,user = request.user)
            videos = Videos.objects.all()
            context = {'videos':videos,'unseen_count':unseen_count,'pers':pers,'notify':notify,'length':len(notify),'unseen_notify':unseen_notify}
            template = loader.get_template('html_ki_file/testvideo2.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
    def post(self,request):
        if request.user.is_authenticated:
            is_repeated = False
            p2 = Preferences.objects.filter(pref = request.POST['preference'],user = request.user)
            if len(p2) == 0:
                p = Preferences(pref = request.POST['preference'],user = request.user)
                p.save()
            else:
                is_repeated = True
            pers = Preferences.objects.filter(user = request.user)
            unseen_count = Notification.objects.filter(seen = False,user = request.user).count()
            notify = Notification.objects.filter(user = request.user)
            videos = Videos.objects.all()
            context = {'videos':videos,'unseen_count':unseen_count,'pers':pers,'notify':notify,'length':len(notify),'is_repeated':is_repeated}
            template = loader.get_template('html_ki_file/testvideo2.html')
            return HttpResponse(template.render(context,request))
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username = username,password=password,is_superuser=False)
            notify = Notification.objects.all()
        #unseen = Notification.objects.filter(seen = False,user = request.user)
        
        
            videos = Videos.objects.all()
            for u in user:
                if u is not None:
                    login(request,u)
                    notify = Notification.objects.filter(user = request.user)
                    pers = Preferences.objects.filter(user = request.user)
                    unseen_count = Notification.objects.filter(seen = False,user = request.user).count()
                    context = {'videos':videos,'unseen_count':unseen_count,'pers':pers,'notify':notify,'length':len(notify)}
                    template = loader.get_template('html_ki_file/testvideo2.html')
                    return HttpResponse(template.render(context,request))
            template = loader.get_template('html_ki_file/login.html')
            context = {'is_alert':True}
            return HttpResponse(template.render(context,request))
            #return HttpResponse("username or password does not match")
        
class Recently(View):
    def get(self,request):
        if request.user.is_authenticated and request.user.is_superuser == False:
            rec_vid = []
            unseen_count = Notification.objects.filter(seen = False,user = request.user).count()
            recent_video = []
            recent_viewed = recently_viewed.objects.filter(user = request.user)
            index = len(recent_viewed)-1
            if index <= 4:
                i = index
            else:
                i = 4
            while i>=0:
                video = Videos.objects.filter(id = recent_viewed[index].videoid)
                if len(video)!= 0:
                    if str(video[0].videofile)[-4::1] == ".mp4":
                        rec_vid.append(video[0])
                    recent_video.append(video[0])
                index = index -1
                i = i -1
            context = {'unseen_count':unseen_count,'recent_videos':recent_video,'length1':len(recent_video),'rec_vid':rec_vid,'length':len(rec_vid)}
            template = loader.get_template('html_ki_file/pdfstudent.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
def Getvideos2(request,parameter):
    recent = recently_viewed(user = request.user,videoid = parameter)
    #recent.videoid = parameter
    recent.save()
    video = Videos.objects.get(id = parameter)
    viewed_user = []
    #thumb = get_thumbnail('/media/' + str(video.videofile), '300x300', crop='center')
    user = User.objects.filter(username = request.user.username,is_superuser = False)
    if len(user)!=0:
        viewed_user = Viewed_user.objects.filter(video = video,user =user[0])
    if len(viewed_user) == 0 and len(user)!= 0:
        v = Viewed_user(video = video,user = user[0])
        v.save()
        video.user_viewed = video.user_viewed +1
        video.save()
    video = Videos.objects.get(id = parameter)
    is_audio = False
    is_image = False
    is_pdf = False
    is_video = False
    if str(video.videofile)[-4::1] == ".ogg":
        is_audio = True
    if str(video.videofile)[-4::1] == ".jpg" or str(video.videofile)[-4::1] == ".png" :
        is_image = True
    if  str(video.videofile)[-4::1] == ".pdf" or str(video.videofile)[-4::1] == ".txt":
        is_pdf = True
    if str(video.videofile)[-4::1] == ".mp4":
        is_video = True
   

    #if str(video.videofile)[-4::1] == ".3gp"
    like = liked_video.objects.filter(video = video,user = request.user)
    if len(like) == 0:
        is_blue = False
    else:
        is_blue = True
    video = Videos.objects.get(id = parameter)
    com = Comment.objects.filter(video = video)
    context = {'video':video,'is_audio':is_audio,'is_blue':is_blue,'is_image':is_image,'is_pdf':is_pdf,'is_video':is_video,'comments':com,'length':len(com),'user':request.user}
    template = loader.get_template('html_ki_file/getvideo3.html')
    return HttpResponse(template.render(context,request))

def Comment2(request,parameter):
    video = Videos.objects.get(id = parameter)
    cmnt = Comment(text = request.POST['comment'],video = video,user = request.user)
    cmnt.save()
    is_audio = False
    is_image = False
    is_pdf = False
    is_video = False
    if str(video.videofile)[-4::1] == ".ogg":
        is_audio = True
    if str(video.videofile)[-4::1] == ".jpg" or str(video.videofile)[-4::1] == ".png" :
        is_image = True
    if  str(video.videofile)[-4::1] == ".pdf" or str(video.videofile)[-4::1] == ".txt":
        is_pdf = True
    if str(video.videofile)[-4::1] == ".mp4":
        is_video = True
   

    #if str(video.videofile)[-4::1] == ".3gp"
    like = liked_video.objects.filter(video = video,user = request.user)
    if len(like) == 0:
        is_blue = False
    else:
        is_blue = True
    video = Videos.objects.get(id = parameter)
    com = Comment.objects.filter(video = video)
    context = {'video':video,'is_audio':is_audio,'is_blue':is_blue,'is_image':is_image,'is_pdf':is_pdf,'is_video':is_video,'comments':com,'length':len(com)}
    template = loader.get_template('html_ki_file/getvideo3.html')
    return HttpResponse(template.render(context,request))
    
class Msg(View):
    def post(self,request):
        to_teacher = request.POST['text1']
        if request.POST['text3'] == "":
            filetype = "any"
        else:
            filetype = request.POST['text3'] 
        if to_teacher == "":
            user = User.objects.filter(is_superuser = True)
        else:
            user = User.objects.filter(username = request.POST['text1'])
            if len(user) == 0:
                return HttpResponse('username does not exist <br> <a href = "../login"> go back </a>')
        for u in user:
            msg = Message(to = u,fom = request.user.username,topic = request.POST['text2'],file = filetype)
            msg.save()
        return HttpResponseRedirect("../login/")
class Show_notification(View):
    def get(self,request):
        unseen_count = Notification.objects.filter(seen = False,user = request.user).count()
        Notify = Notification.objects.all()
        unseen_noti = Notification.objects.filter(seen = False,user = request.user)
        seen_noti = Notification.objects.filter(seen = True,user = request.user)
        Notification.objects.all().delete()
        #context = {'len_noti':len(Notify),'unseen_noti':unseen_noti,'seen_noti':seen_noti,'unseen_count':unseen_count}
        #template = loader.get_template('html_ki_file/shownotify.html')
        #return HttpResponse(template.render(context,request))
        return HttpResponseRedirect("../login/")

class Main(View):
    def get(self,request):
        if request.user.is_authenticated:
            context={'nodata':'nodata'}
            template = loader.get_template('html_ki_file/main.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse('login first')

class Menu(View):
    
    
    def get(self,request):
        search_value = 'none'
        url_of_video_student = []
        url_of_video_teacher = []
        
        
        if request.user.is_authenticated:
            if request.user.is_superuser == False:
                videos = Videos.objects.all().order_by('-user_viewed')
                for v in videos:
                    score = liked_video.objects.filter(video = v).count()
                    v.votes = score
                    v.save()
                videos = Videos.objects.all().order_by('-votes')
                
                for video in videos:
                    i = -1
                    string = str(video.videofile)
                    while(string[i] != '.'):
                        i = i-1
                    if string[i+1:] == "mp4" or string[i+1:] == "3gp":
                        url_of_video_student.append(video)
                context = {'is_superuser':False,'videos':url_of_video_student,'length':len(url_of_video_student),'search_value':search_value}
                template = loader.get_template('html_ki_file/menu.html')
                return HttpResponse(template.render(context,request))
                
            videos = Videos.objects.filter(user = request.user)
            for v in videos:
                    score = liked_video.objects.filter(video = v).count()
                    v.votes = score
                    v.save()
            videos = Videos.objects.filter(user = request.user).order_by('-votes')
            for video in videos:
                i = -1
                string = str(video.videofile)
                while(string[i] != '.'):
                    i = i-1
                if string[i+1:] == "mp4" or string[i+1:] == "3gp":
                    url_of_video_teacher.append(video)
            context = {'is_superuser':True,'videos':url_of_video_teacher,'length':len(url_of_video_teacher),'search_value':search_value}
            template = loader.get_template('html_ki_file/menu.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse('login first')
    def post(self,request):
        url_of_video_student = []
        url_of_video_teacher = []
        if request.user.is_authenticated:
            search_value = request.POST['searching']
            videos1 = []
            if request.user.is_superuser == False:
                videos = Videos.objects.all().order_by('-votes')
                for video in videos:
                    i = -1
                    string = str(video.videofile)
                    while(string[i] != '.'):
                        i = i-1
                    if string[i+1:] == "mp4" or string[i+1:] == "3gp":
                        url_of_video_student.append(video)
                for vid in url_of_video_student:
                    if vid.title == request.POST['searching'].title():
                        videos1.append(vid)
                    else:
                        T = str(vid.title).split(" ")
                        for t in T:
                            if t == request.POST['searching'].title():
                              videos1.append(vid)
                              break
                context = {'is_superuser':False,'videos':videos1,'length':len(videos1),'search_value':search_value}
                template = loader.get_template('html_ki_file/menu.html')
                return HttpResponse(template.render(context,request))
            if request.user.is_superuser == True:
                videos = Videos.objects.filter(user = request.user)
                for video in videos:
                    i = -1
                    string = str(video.videofile)
                    while(string[i] != '.'):
                        i = i-1
                    if string[i+1:] == "mp4" or string[i+1:] == "3gp":
                        url_of_video_teacher.append(video)
                for vid in url_of_video_teacher:
                    if vid.title == request.POST['searching'].title():
                        videos1.append(vid)
                    else:
                        T = str(vid.title).split(" ")
                        for t in T:
                            if t == request.POST['searching'].title():
                              videos1.append(vid)
                              break
                        """
                        i = 0
                        while(i != len(vid.title)):
                            while(vid.title[i] != " "):
                                i = i+1
                            if vid.title[:i] == request.POST['searching'].title():
                                videos1.append(vid)
                                break
                        """
                context = {'is_superuser':True,'videos':videos1,'length':len(videos1),'search_value':search_value}
                template = loader.get_template('html_ki_file/menu.html')
                return HttpResponse(template.render(context,request))
        
class Header(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser == False:
                unseen_count = Notification.objects.filter(seen = False,user = request.user).count()
                context={'is_superuser':False,'unseen_count':unseen_count}
                template = loader.get_template('html_ki_file/header.html')
                return HttpResponse(template.render(context,request))
                
            unseen = Message.objects.filter(to = request.user ,seen = False)
            unseen_count = unseen.count()
            context={'is_superuser':True,'unseen_count':unseen_count}
            template = loader.get_template('html_ki_file/header.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse('login first')

class Menupdf(View):
    
    def get(self,request):
        search_value = 'none'
        if request.user.is_authenticated:
            if request.user.is_superuser == False:
                videos = Videos.objects.all().order_by('-user_viewed')
                for v in videos:
                    score = liked_video.objects.filter(video = v).count()
                    v.votes = score
                    v.save()
                videos = Videos.objects.all().order_by('-votes')
                url_of_pdf = []
                for video in videos:
                    string = str(video.videofile)
                    if string[-3::1] == "pdf":
                        url_of_pdf.append(video)
                context = {'is_superuser':False,'pdfs':url_of_pdf,'len_pdf':len(url_of_pdf),'search_value':search_value}
                template = loader.get_template('html_ki_file/menupdf.html')
                return HttpResponse(template.render(context,request))
                
            videos = Videos.objects.filter(user = request.user)
            for v in videos:
                    score = liked_video.objects.filter(video = v).count()
                    v.votes = score
                    v.save()
            videos = Videos.objects.filter(user = request.user).order_by('-votes')
            url_of_pdf = []
            for video in videos:
                string = str(video.videofile)
                if string[-3::1] == "pdf":
                    url_of_pdf.append(video)
            context = {'is_superuser':True,'pdfs':url_of_pdf,'len_pdf':len(url_of_pdf),'search_value':search_value}
            template = loader.get_template('html_ki_file/menupdf.html')
            return HttpResponse(template.render(context,request))
        else:
            return HttpResponse("login first")
    def post(self,request):
        search_value = request.POST['searching']
        videos1 = []
        videos2 = dict()
        page_no = []
        if request.user.is_superuser == False:
            videos = Videos.objects.all().order_by('-votes')
            url_of_pdf = []
            for video in videos:
                string = str(video.videofile)
                if string[-3::1] == "pdf":
                    url_of_pdf.append(video)
            for vid in url_of_pdf:
                    if vid.title == request.POST['searching'].title():
                        videos1.append(vid)
            for vid in url_of_pdf:
                if vid in videos1:
                    pass
                else:
                    T = str(vid.title).split(" ")
                    for t in T:
                        if t == request.POST['searching'].title():
                            videos1.append(vid)
                            break
            #flag2 = ""
            for vid in url_of_pdf:
                if vid in videos1:
                    pass
                else:
                    #import fitz
                    name = request.POST['searching']
                    name = name.split()
                    name = list(map(lambda x:x.lower(),name)) 
                    length = len(name)
                    pdf_document = "media/" + str(vid.videofile)
                    doc = fitz.open(pdf_document)
                    num_page = doc.pageCount
                    for i in range(0,num_page):
                        #flag2 = "in i loop"
                        flag = False
                        page1 = doc.loadPage(i)
                        page1_list = page1.getText("text").split()
                        page1_list = list(map(lambda x:x.lower(),page1_list))
                        for k in range(0,len(page1_list)):
                            if name == page1_list[k:k+length:1]:
                                page_no.append(i)
                                #flag2 = "found"
                                videos2[vid] = i
                                flag = True
                                break
                        if flag:
                            break
            """
            if len(videos2) == 0:
                search_value = "none"
            else:
                search_value = request.POST['searching']
            """
            videos1
            context = {'is_superuser':False,'pdfs':videos1,'pdfs2':videos2,'len_pdf':len(videos1),'search_value':search_value,'len_pdf2':len(videos2),'pages':page_no}
            template = loader.get_template('html_ki_file/menupdf.html')
            return HttpResponse(template.render(context,request))
            #return HttpResponse("hey" + flag2)
        else:
            videos = Videos.objects.filter(user = request.user)
            url_of_pdf = []
            for video in videos:
                string = str(video.videofile)
                if string[-3::1] == "pdf":
                    url_of_pdf.append(video)
            for vid in url_of_pdf:
                if vid.title == request.POST['searching'].title():
                    videos1.append(vid)
            for vid in url_of_pdf:
                if vid in videos1:
                    pass
                else:
                    T = str(vid.title).split(" ")
                    for t in T:
                        if t == request.POST['searching'].title():
                            videos1.append(vid)
                            break
            for vid in url_of_pdf:
                if vid in videos1:
                    pass
                else:
                    #import fitz
                    name = request.POST['searching']
                    name = name.split()
                    name = list(map(lambda x:x.lower(),name)) 
                    length = len(name)
                    pdf_document = "media/" + str(vid.videofile)
                    doc = fitz.open(pdf_document)
                    num_page = doc.pageCount
                    for i in range(0,num_page):
                        #flag2 = "in i loop"
                        flag = False
                        page1 = doc.loadPage(i)
                        page1_list = page1.getText("text").split()
                        page1_list = list(map(lambda x:x.lower(),page1_list))
                        for k in range(0,len(page1_list)):
                            if name == page1_list[k:k+length:1]:
                                #flag2 = "found"
                                videos2[vid] = i
                                flag = True
                                break
                        if flag:
                            break
            """
            if len(videos2) == 0:
                search_value = "none"
            else:
                search_value = request.POST['searching']
            """
            videos1
            context = {'is_superuser':False,'pdfs':videos1,'pdfs2':videos2,'len_pdf':len(videos1),'search_value':search_value,'len_pdf2':len(videos2),'pages':page_no}
            template = loader.get_template('html_ki_file/menupdf.html')
            return HttpResponse(template.render(context,request))
            """
            videos1.extend(videos2)
            context = {'is_superuser':True,'pdfs':videos1,'len_pdf':len(videos1),'search_value':search_value}
            template = loader.get_template('html_ki_file/menupdf.html')
            return HttpResponse(template.render(context,request))
            """
class Sortmenu(View):
    def get(self,request):
        if request.user.is_superuser == True:
            is_superuser = True
            videos = Videos.objects.filter(user = request.user).order_by('size')
        else:
            is_superuser = False
            videos = Videos.objects.all().order_by('size')
        url_of_video_student = []
        search_value = 'none'
        
        for video in videos:
            i = -1
            string = str(video.videofile)
            while(string[i] != '.'):
                i = i-1
            if string[i+1:] == "mp4":
                url_of_video_student.append(video)
        context = {'is_superuser':is_superuser,'videos':url_of_video_student,'length':len(url_of_video_student),'search_value':search_value,'is_sorted':True}
        template = loader.get_template('html_ki_file/menu.html')
        return HttpResponse(template.render(context,request))
class Sortpdf(View):
    def get(self,request):
        if request.user.is_superuser == True:
            is_superuser = True
            videos = Videos.objects.filter(user = request.user).order_by('size')
        else:
            is_superuser = False
            videos = Videos.objects.all().order_by('size')
        url_of_video_student = []
        search_value = 'none'
        
        for video in videos:
            i = -1
            string = str(video.videofile)
            while(string[i] != '.'):
                i = i-1
            if string[i+1:] == "pdf":
                url_of_video_student.append(video)
        context = {'is_superuser':is_superuser,'pdfs':url_of_video_student,'len_pdf':len(url_of_video_student),'search_value':search_value,'is_sorted':True}
        template = loader.get_template('html_ki_file/menupdf.html')
        return HttpResponse(template.render(context,request))
    
        
            
class Delete(View):
    def get(self,request):
        if request.user.is_authenticated:
            data = request.GET['q']
            datalist = data.split()
            is_audio = False
            is_video = False
            is_image = False
            is_pdf = False
            if datalist[0] == "page":
                video = Videos.objects.get(id = datalist[1])
                page_no = int(datalist[2]) + 1
                recent = recently_viewed(user = request.user,videoid = int(datalist[1]))
    #recent.videoid = parameter
                recent.save()
                video = Videos.objects.get(id = int(datalist[1]))
                viewed_user = []
    #thumb = get_thumbnail('/media/' + str(video.videofile), '300x300', crop='center')
                user = User.objects.filter(username = request.user.username,is_superuser = False)
                if len(user)!=0:
                    viewed_user = Viewed_user.objects.filter(video = video,user =user[0])
                if len(viewed_user) == 0 and len(user)!= 0:
                    v = Viewed_user(video = video,user = user[0])
                    v.save()
                    video.user_viewed = video.user_viewed +1
                    video.save()
                video = Videos.objects.get(id = int(datalist[1]))
                is_audio = False
                is_image = False
                is_pdf = False
                is_video = False
                if str(video.videofile)[-4::1] == ".ogg":
                    is_audio = True
                if str(video.videofile)[-4::1] == ".jpg" or str(video.videofile)[-4::1] == ".png" :
                    is_image = True
                if  str(video.videofile)[-4::1] == ".pdf" or str(video.videofile)[-4::1] == ".txt":
                    is_pdf = True
                if str(video.videofile)[-4::1] == ".mp4":
                    is_video = True
   

                    #if str(video.videofile)[-4::1] == ".3gp"
                like = liked_video.objects.filter(video = video,user = request.user)
                if len(like) == 0:
                    is_blue = False
                else:
                    is_blue = True
                video = Videos.objects.get(id = int(datalist[1]))
                com = Comment.objects.filter(video = video)
                context = {'video':video,'page_no':page_no,'is_audio':is_audio,'is_blue':is_blue,'is_image':is_image,'is_pdf':is_pdf,'is_video':is_video,'comments':com,'length':len(com),'user':request.user}
                template = loader.get_template('html_ki_file/getvideo4.html')
                return HttpResponse(template.render(context,request))
            if(datalist[0] == "not"):
                notif = Notification.objects.get(id = int(datalist[1]))
                file = str(notif.video.videofile)[-4::1]
                notif.delete()
                if  file == ".mp4":
                    return HttpResponseRedirect("../home2")
                if file == ".pdf":
                    return HttpResponseRedirect("../getpdf")
            
                
            if(datalist[0] == "sort"):
                
                search_value = 'none'
                if datalist[1] == "1":
                    if datalist[2] == "none":
                        pass
                    else:
                        search_value = datalist[2]
                        
                        
                context = {'is_superuser':False,'search_value':search_value}
                template = loader.get_template('html_ki_file/newvideo.html')
                return HttpResponse(template.render(context,request))
            if(datalist[0] == "sortpdf"):
                search_value = ''
                if len(datalist) > 3:
                    for i in range(2,len(datalist)):
                        search_value = search_value + " " + datalist[i]
                else:
                    search_value = datalist[2]
                
                is_pdf = True
                context = {'is_pdf':is_pdf,'is_superuser':False,'search_value':search_value}
                template = loader.get_template('html_ki_file/newvideo.html')
                return HttpResponse(template.render(context,request))
                
            if(datalist[0] == "sort2"):
                if request.user.is_superuser == True:
                    is_superuser = True
                    videos = Videos.objects.filter(user = request.user).order_by('size')
                else:
                    is_superuser = False
                    videos = Videos.objects.all().order_by('size')
                search_value = datalist[1]
                
                videos1 = []
                url_of_video_student = []
                
                for video in videos:
                    i = -1
                    string = str(video.videofile)
                    while(string[i] != '.'):
                        i = i-1
                    if string[i+1:] == "mp4" or string[i+1:] == "3gp":
                        url_of_video_student.append(video)
                for vid in url_of_video_student:
                    if vid.title == search_value.title():
                        videos1.append(vid)
                    else:
                        T = str(vid.title).split(" ")
                        for t in T:
                            if t == search_value.title():
                              videos1.append(vid)
                              break
                context = {'is_superuser':is_superuser,'videos':videos1,'length':len(videos1),'search_value':search_value,'is_sorted':True}
                template = loader.get_template('html_ki_file/menu.html')
                return HttpResponse(template.render(context,request))
                #return HttpResponse("undelete" + datalist[1])
            if(datalist[0] == "sort2pdf"):
                search_value = ''
                if request.user.is_superuser == True:
                    is_superuser = True
                    videos = Videos.objects.filter(user = request.user).order_by('size')
                else:
                    is_superuser = False
                    videos = Videos.objects.all().order_by('size')
                if len(datalist) > 2:
                    for i in range(1,len(datalist)):
                        search_value = search_value + " " + datalist[i]
                else:
                    search_value = datalist[1]
                
                videos1 = []
                videos2 = dict()
                page_no = []
                url_of_video_student = []
                
                for video in videos:
                    i = -1
                    string = str(video.videofile)
                    while(string[i] != '.'):
                        i = i-1
                    if string[i+1:] == "pdf":
                        url_of_video_student.append(video)
                for vid in url_of_video_student:
                    if vid.title == search_value.title():
                        videos1.append(vid)
                for vid in url_of_video_student:
                    if vid in videos1:
                        pass
                    else:
                   
                        T = str(vid.title).split(" ")
                        for t in T:
                            if t == search_value.title():
                              videos1.append(vid)
                              break
                for vid in url_of_video_student:
                    if vid in videos1:
                        pass
                    else:
                        #import fitz
                        name = search_value
                        name = name.split()
                        name = list(map(lambda x:x.lower(),name)) 
                        length = len(name)
                        pdf_document = "media/" + str(vid.videofile)
                        doc = fitz.open(pdf_document)
                        num_page = doc.pageCount
                        for i in range(0,num_page):
                            #flag2 = "in i loop"
                            flag = False
                            page1 = doc.loadPage(i)
                            page1_list = page1.getText("text").split()
                            page1_list = list(map(lambda x:x.lower(),page1_list))
                            for k in range(0,len(page1_list)):
                                if name == page1_list[k:k+length:1]:
                                    page_no.append(i)
                                    #flag2 = "found"
                                    videos2[vid] = i
                                    flag = True
                                    break
                            if flag:
                                break
                """
                if len(videos2) == 0:
                    search_value = "none"
                """
                videos1
                context = {'is_superuser':False,'pdfs':videos1,'pdfs2':videos2,'len_pdf':len(videos1),'search_value':search_value,'len_pdf2':len(videos2),'pages':page_no}
                template = loader.get_template('html_ki_file/menupdf.html')
                return HttpResponse(template.render(context,request))

                """
                videos1.extend(videos2)
                context = {'is_superuser':is_superuser,'pdfs':videos1,'len_pdf':len(videos1),'search_value':search_value,'is_sorted':True}
                template = loader.get_template('html_ki_file/menupdf.html')
                return HttpResponse(template.render(context,request))
                """
                        
            if(datalist[0] == "likevideo"):
                    video = Videos.objects.get(id = int(datalist[1]))
                    l = liked_video(video = video,user = request.user)
                    l.save()
                    is_video = True
                    context = {'idd':video.id,'show':True,'nodata':'nodatata','is_image':is_image,'is_audio':is_audio,'is_video':is_video,'is_pdf':is_pdf}
                    template = loader.get_template('html_ki_file/getvideo.html')
                    return HttpResponse(template.render(context,request))
            if(datalist[0] == "likepdf"):
                    video = Videos.objects.get(id = int(datalist[1]))
                    l = liked_video(video = video,user = request.user)
                    l.save()
                    is_pdf = True
                    context = {'idd':video.id,'show':True,'nodata':'nodatata','is_image':is_image,'is_audio':is_audio,'is_video':is_video,'is_pdf':is_pdf}
                    template = loader.get_template('html_ki_file/getvideo.html')
                    return HttpResponse(template.render(context,request))
            if datalist[0] == "dislikevideo":
                video = Videos.objects.get(id = int(datalist[1]))
                liked_video.objects.filter(video = video,user = request.user).delete()
                is_video = True
                context = {'idd':video.id,'show':True,'nodata':'nodatata','is_image':is_image,'is_audio':is_audio,'is_video':is_video,'is_pdf':is_pdf}
                template = loader.get_template('html_ki_file/getvideo.html')
                return HttpResponse(template.render(context,request))
            if datalist[0] == "dislikepdf":
                video = Videos.objects.get(id = int(datalist[1]))
                liked_video.objects.filter(video = video,user = request.user).delete()
                is_pdf = True
                context = {'idd':video.id,'show':True,'nodata':'nodatata','is_image':is_image,'is_audio':is_audio,'is_video':is_video,'is_pdf':is_pdf}
                template = loader.get_template('html_ki_file/getvideo.html')
                return HttpResponse(template.render(context,request))
            if datalist[0] == "deletecmnt":
                cmnt = Comment.objects.get(id = int(datalist[1]))
                video = Videos.objects.get(id = cmnt.video.id)
                cmnt.delete()
                is_audio = False
                is_image = False
                is_pdf = False
                is_video = False
                if str(video.videofile)[-4::1] == ".ogg":
                    is_audio = True
                if str(video.videofile)[-4::1] == ".jpg" or str(video.videofile)[-4::1] == ".png" :
                    is_image = True
                if  str(video.videofile)[-4::1] == ".pdf" or str(video.videofile)[-4::1] == ".txt":
                    is_pdf = True
                if str(video.videofile)[-4::1] == ".mp4":
                    is_video = True
                context = {'idd':video.id,'show':True,'nodata':'nodatata','is_image':is_image,'is_audio':is_audio,'is_video':is_video,'is_pdf':is_pdf}
                template = loader.get_template('html_ki_file/getvideo.html')
                return HttpResponse(template.render(context,request))
                
                
            if datalist[0] == "msg":
                for idd in datalist[1:]:
                    if idd != 'undefined':
                        msg = Message.objects.filter(id = int(idd))
                        if len(msg)!=0:
                            msg.delete()
                return HttpResponseRedirect("showmsg")
            if datalist[0] == "pref":
                for idd in datalist[1:]:
                    if idd != 'undefined':
                        pref = Preferences.objects.filter(id = int(idd))
                        if len(pref)!=0:
                            pref.delete()
                
                return HttpResponseRedirect("login")
            else:
                for idd in datalist[1:]:
                    if idd != 'undefined':
                        video = Videos.objects.filter(id = int(idd))
                        if len(video)!=0:
                            video.delete()
                if(datalist[0] == "0"):
                    return HttpResponseRedirect("getvideo/")
                if(datalist[0] == "1"):
                    return HttpResponseRedirect("getimages/")
                if(datalist[0] == "2"):
                    return HttpResponseRedirect("getpdf/")
                if(datalist[0] == "3"):
                    return HttpResponseRedirect("getaudio/")
                
        else:
            return HttpResponse("loginfirst")




    
