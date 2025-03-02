from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('home',views.home,name='home'),

    # """ dataowner urls"""

    path('do',views.dataowner,name='do'),
    path('login',views.dologin,name='dologin'),
    path('viewprofile',views.viewprofile,name='viewprofile'),
    path('uploadfile',views.uploadfiles,name='uploadfiles'),
    path('viewfile',views.viewfile,name='viewfile'),
    path('dologout',views.dologout,name='dologout'),

    # """ Data Consumer urls"""

    path('datauser', views.datauser, name='datauser'),
    path('userlogin', views.userlogin, name='userlogin'),
    path('getdata/<str:filename>/<str:Dataowner>', views.getdata, name='getdata'),
    path('viewfiles', views.viewfiles, name='viewfiles'),
    path('sendreq/<int:id>',views.sendreq,name='sendreq'),
    path('viewres',views.viewres,name='viewres'),
    path('fileview/<int:id>/<str:filename>/',views.fileview, name='fileview'),
    path('keyfile',views.keyfile,name='keyfile'),
    path('enfile',views.enfile,name='enfile'),
    path('dulogout',views.dulogout,name='dulogout'),


    # """ Cloud service provider urls """

    path('CloudServiceProvider',views.CloudServiceProvider,name='CloudServiceProvider'),
    path('data',views.data,name='data'),
    path('viewdataownerfiles',views.viewdataownerfiles,name='viewdataownerfiles'),
    path('ado/<int:id>',views.ado,name='ado'),
    path('viewss',views.viewss,name='viewss'),
    path('getdata/<int:id>/<str:Dataowner>/<str:filename>/<str:datauser>/',views.getdata,name='getdata'),
    path('stt',views.stt,name='stt'),
    path('sentdata/<str:filename>/<str:Dataowner>',views.sentdata,name='sentdata'),
    path('csplogout',views.csplogout,name='csplogout'),





    # """ central Authority urls """

    path('cloudauthority',views.cloudauthority,name='cloudauthority'),
    path('alldatausers',views.alldatausers,name='alldatausers'),
    path('adc/<int:id>',views.adc,name='adc'),
    path('reqview',views.reqview,name='reqview'),
    path('send/<str:fileid>',views.send,name='send'),
    path("linkdata/<str:filename>/<str:datauser>",views.linkdata,name='linkdata'),
    path('calogout',views.calogout,name='calogout'),

    # """ Attribute Authority urls """

    path('attributeauthority',views.attributeauthority,name='attributeauthority'),
    path('vifi',views.vifi,name='vifi'),
    path('vireq',views.vireq,name='vireq'),
    path('update/<str:Name>/<str:Email>',views.update,name='update'),
    path('viewdo',views.viewdo,name='viewdo'),
    path('vidureq',views.vidureq,name='vidureq'),
    path('sendkey/<str:datauser>/<int:key>',views.sendkey,name='sendkey'),
    # path('valdata/<str:Datauser>/<str:filename>/',views.valdata,name='valdata'),
    path('aalogout',views.aalogout,name='aalogout')


]