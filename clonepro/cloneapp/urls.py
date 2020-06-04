from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.urls import path , include
from django.views.generic.base import TemplateView
from . import views
from cloneapp.views import First, Addlink, Sortmenu , Sortpdf, Delete, Recently, Recently1,Comment2, Home ,Getvideos ,Getpdf,Videoupload,Msg ,Login ,Showmsg,Show_notification,Main,Menu,Header,Menupdf
app_name = 'cloneapp'

urlpatterns =[
    path('addlink',Addlink.as_view(),name='addlink'),
    path('showmsg',Showmsg.as_view(),name='showmsg'),
    path('start/',views.start,name = 'start'),
    path('login/',Login.as_view(),name = 'login'),
    path('recent/',Recently.as_view(),name = 'recent'),
    path('sortmenu/',Sortmenu.as_view(),name = 'sortmenu'),
    path('sortpdf/',Sortpdf.as_view(),name = 'sortpdf'),
    path('recent1/',Recently1.as_view(),name = 'recently'),
    
    path('form/',views.viewuser,name = 'viewuser'),
    path('signin/',views.signin,name = 'signin'),
    path('first/',First.as_view(),name = 'First'),
    path('home/',Home.as_view(),name = 'home'),
    path('getvideo/',Getvideos.as_view(),name = 'getvideo'),
    path('getpdf/',Getpdf.as_view(),name = 'getpdf'),
    path('upload/',Videoupload.as_view(),name = 'upload'),
    path('form2/',views.viewuser2,name = 'viewuser2'),

    path('home2/',Getvideos.as_view(),name = 'home2'),
    url(r'comment/(?P<parameter>[0-9]+)/$',views.Comment2,name = 'comment'),
    
    #path('home3/',Home3.as_view(),name = 'home3'),
    path('msg/',Msg.as_view(),name = 'msg'),
    url(r'home2/(?P<parameter>[0-9]+)/$',views.Getvideos2,name = 'getvideo'),
    url(r'home3/(?P<parameter>[0-9]+)/$',views.Getvideos2,name = 'getvideo'),
    path(r'getpdf/',Getpdf.as_view(),name='pdfstudent'),
    path(r'shownotify',Show_notification.as_view(),name='shownotify'),
    path(r'main',Main.as_view(),name='main'),
    path(r'menu',Menu.as_view(),name='menu'),
    path(r'menupdf',Menupdf.as_view(),name='menupdf'),
    #path(r'menuaudio',Menuaudio.as_view(),name='menuaudio'),
    path(r'header',Header.as_view(),name='header'),
    url(r'^$',Delete.as_view(),name='delete'),
    
    ]

