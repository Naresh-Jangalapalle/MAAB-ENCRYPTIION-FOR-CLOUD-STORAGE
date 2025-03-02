from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from .models import Datauserregistration,Datauserrequest,dataownerreg,uploadfile,Cloudserviceprovider,AttributeAuthority,attribute,datauser_values
#
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
import datetime
date=datetime.datetime.now()
from django.db import connection
cursor = connection.cursor()
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



import binascii
import random

from django.db import connection
from django.contrib.sessions.models import Session
import pandas as pd
from django.conf import settings
from django.core.mail import send_mail
from datetime import date

today = date.today()

def home(request):
    return render(request,'index.html')

#  data owner session
def dataowner(request):
    if request.method=='POST':
        data.Name=request.POST['Name']
        data.Email=request.POST['Email']
        data.password=request.POST['password']
        data.conpasword=request.POST['conpassword']
        data.status='pending'
        if data.password == data.conpasword:
            dc = dataownerreg.objects.filter(Name=data.Name,password=data.password).exists()
            if dc:
                messages.success(request,"User Already Exists")
                return render(request,'reg.html')
            else:
                dc = dataownerreg(Name=data.Name, Email=data.Email, password=data.password, status=data.status)
                dc.save()
                return render(request, 'login.html')
        else:
            messages.success(request,"Passwords Are not Matched")
            return render(request,'reg.html')
    return render(request,'reg.html')

def dologin(request):
    if request.method=='POST':
        Name=request.POST['Name']
        request.session['Name']=Name
        password=request.POST['password']
        print(Name,password)
        dc = dataownerreg.objects.filter(Name=Name,password=password,status='approved').exists()
        if dc:
            request.session['dataowner'] = Name
            return render(request, 'loghome.html')
        else:
            messages.success(request, "Invalid Credentials")
            return render(request, 'login.html')
    return render(request, 'login.html')

def viewprofile(request):
    dc = dataownerreg.objects.filter(Name=request.session['Name'])
    
    return render(request,'viewprofile.html',{'dc':dc})

def uploadfiles(request):
    global nonce,tag
    if request.method=="POST":
       file= request.FILES['filename']
       filedata=file.read()
       nonce=random.randint(1,100)
       d=today.strftime("%d/%m/%Y")
       
       sql ="insert into app_uploadfile(filename,Dataowner,date,filepath,ciphertext,nounce) values(%s,%s,%s,%s,AES_ENCRYPT(%s, 'secretkey'),%s)"
       val=(file,request.session['Name'],d,file,filedata,str(nonce))
       cursor.execute(sql,val)
       connection.commit()
       messages.success(request,'File uploaded successfully')
       return render(request, 'upload.html')
    return render(request,'upload.html')


def viewfile(request):
    dc = uploadfile.objects.filter(Dataowner=request.session['Name']).values('id','filename','ciphertext','date')
    return render(request,'viewfile.html',{'dc':dc})


def dologout(request):
    Session.objects.all().delete()
    return render(request,'index.html')

# data user session

def datauser(request):
    if request.method=='POST':
        infor=Datauserregistration()
        infor.Name=request.POST['name']
        infor.Email=request.POST['email']
        infor.password=request.POST['passcode']
        infor.conpasword=request.POST['Conpasscode']

        if infor.password == infor.conpasword:

            if Datauserregistration.objects.filter(Name=request.POST['name'],Email=request.POST['email']).exists():
                messages.info(request,'Email Exists')
                return render(request, 'userreg.html')
            else:
                d = today.strftime("%d/%m/%Y")
                dc = Datauserregistration(Name=infor.Name, Email=infor.Email, password=infor.password)
                dc.save()
                return render(request, 'userlogin.html')
        else:
            messages.success(request,"Passwords Are not Matched")
            return render(request,'userreg.html')
    return render(request,'userreg.html')

def userlogin(request):
    if request.method=='POST':
        Name=request.POST['name']
        request.session['username']=Name
        password=request.POST['password']
        if Datauserregistration.objects.filter(Name=Name,password=password,status='approved').exists():
            return render(request, 'userloghome.html')
        else:
            messages.success(request, "Invalid Credentials")
            return render(request, 'userlogin.html')
    return render(request, 'userlogin.html')

def viewfiles(request):
    data=uploadfile.objects.all()
    return render(request,'viewfiles.html',{'dc':data})

def sendreq(request,id):
    tt = today
    dc = uploadfile.objects.filter(id=id)
    data = [(i.id,i.filename) for i in dc]
    dc = Datauserrequest(fileid=data[0][0],datauser=request.session['username'],filename=data[0][1],status='pending',date=tt)
    dc.save()
    messages.info(request,'request sent successfully')
    return redirect('viewfiles')

def getdata(request,filename,Dataowner):
    tt = date.strftime("%I:%M %p")
    
    sql="insert into app_cloudserviceprovider(filename,date,dataowner,datauser)values(%s,%s,%s,%s)"
    val=(filename,tt,Dataowner,request.session['username'])
    cur.execute(sql,val)
    connection.commit()
    sql="update app_uploadfile set datauser=%s where filename=%s and Dataowner=%s"
    val=(request.session['username'],filename,Dataowner)
    cur.execute(sql,val)
    connection.commit()
    messages.success(request,"request sended to CloudService Provider")
    return redirect('viewfiles')


def viewres(request):
    val=Datauserrequest.objects.filter()
    return render(request,'res.html',{'data':val})

def fileview(request,id,filename):
    dc = uploadfile.objects.filter(id=id,filename=filename)
    
    # data=uploadfile.objects.all()
    return render(request,'fileview.html',{'id':id,'filename':filename})



def keyfile(request):
    if request.method == 'POST':
        id = request.POST['id']
        filename = request.POST['filename']
        e = request.POST['Message']
        print(e)
        dc = Datauserrequest.objects.filter(key=e).exists()
        if dc:
            sql = "select AES_DECRYPT(ciphertext,'secretkey') from app_uploadfile where id=%s"%(id)
            cursor.execute(sql)
            data = cursor.fetchall()
            connection.commit()
            data = data[0][0]
            data = data.decode()
            return render(request, 'viewdata.html', {'data': data})
        else:
            messages.info(request, 'invalid key')
            return redirect("viewres")


def enfile(request):
    return render(request,'enfile.html')




def dulogout(request):
    Session.objects.all().delete()
    return render(request,'index.html')


# Cloud service provider

def CloudServiceProvider(request):
    if request.method=='POST':
        name=request.POST['Name']
        request.session['csp']=name
        Password=request.POST['Password']
        if name=='CSP' and Password=="CSP":
            return render(request,'csploghome.html')
        messages.info(request,'invalid details')
        return render(request, 'csplogin.html')
    return render(request,'csplogin.html')

def data(request):
    dc = dataownerreg.objects.all()
    return render(request,"csp.html",{'dc':dc})


def viewdataownerfiles(request):
    dc=uploadfile.objects.all()
    return render(request,'viewdataownerfiles.html',{'dc':dc})

def ado(request,id):
    dc = dataownerreg.objects.get(id=id,status='pending')
    dc.status='approved'
    dc.save()
    return redirect(data)

def viewss(request):
    data=uploadfile.objects.all()
    return render(request,'viewss.html',{'val':data})


def getdata(request,id,Dataowner,filename,datauser):
    print(id,Dataowner,filename,datauser)
    d3 = today.strftime("%d/%m/%Y")
    sql="insert into app_attribute(Dataowner,filename,Datauser,date) values ('%s','%s','%s','%s')" %(Dataowner,filename,datauser,d3)
    cur.execute(sql)
    connection.commit()
    messages.info(request,'Request sent to Attribute Authority')

    return redirect(viewss)



def sentdata(request,filename,Dataowner):
    at = date.strftime("%I:%M %p")
    sql="insert into app_attributeauthority(Dataowner,filename,date)values(%s,%s,%s)"
    val=(Dataowner,filename,at)
    cur.execute(sql,val)
    connection.commit()
    sql="update app_attributeauthority set status='access' where status='status' and filename='%s' "%(filename)
    cur.execute(sql)
    connection.commit()
    # data=AttributeAuthority.objects.all()
    return redirect('data')
    # return render(request,'sentdata.html')

def csplogout(request):
    return render(request,'index.html')

# def index(request):
#     return render(request,'index.html')


# cloud Authority


def cloudauthority(request):
    if request.method=='POST':
        name=request.POST['val1']
        password=request.POST['val2']
        print(name,password)
        if name=="CA" and password=='CA':

            return render(request,'cloudauthorityhome.html')

    return render(request,'cloudauthoritylog.html')


def alldatausers(request):
    data=Datauserregistration.objects.all()
    return render(request,'alldatausers.html',{'data':data})

def adc(request,id):
    data=Datauserregistration.objects.get(id=id,status='pending')
    data.status='approved'
    data.save()
    return redirect(alldatausers)


def reqview(request):
    data=Datauserrequest.objects.all()
    return render(request,"viewrequests.html",{'data':data})


def send(request,fileid):
    val = random.randint(000000, 999999)
    data=Datauserrequest.objects.get(fileid=fileid)
    data.key=val
    data.save()
    # sql="select * from app_datauserregistration where Name='%s'"%(request.session['username'])
    # cur.execute(sql)
    # y=cur.fetchall()
    # connection.commit()
    # print(y)
    # z = [i for j in y for i in j]
    # Datauser=z[1]
    # sql="select * from app_uploadfile where keypair='%s'"%(keypair)
    # cur.execute(sql)
    # x=cur.fetchall()
    # connection.commit()
    # m=[i for j in x for i in j]
    # filename=m[1]
    # subject = 'Private Key'
    # message = f'Hi {Datauser}'
    # cont = 'The private key to decrypt file.'

    # KEY=m[-3]
    # m1 = "This message is automatic generated so dont reply to this Mail"
    # m2 = "Thanking you"
    # m3 = "Regards"
    # m4 = "Cloud Service Provider."
    # Email=z[2]
    # print(KEY)
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [Email]
    # text = message + '\n' + KEY + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
    # send_mail(subject, text, email_from, recipient_list,fail_silently=False,)
    # from datetime import date

    # today = date.today()
    # print(today)

    # status='Accepted'
    # sql="insert into app_attribute(filename,Email,date,keypair,status) values(%s,%s,%s,%s,%s)"
    # val=(filename,Email,today,KEY,status)
    # cur.execute(sql,val)
    # connection.commit()


    messages.info(request, 'request sent to Attribute Autghority')
    return redirect('reqview')

def linkdata(request,filename,datauser):

    sql="insert into app_attribute(Dataowner,filename,Datauser) values (%s,%s,%s)"
    val=( request.session['username'],filename,datauser)
    cur.execute(sql,val)
    connection.commit()
   
    return redirect('reqview')

def calogout(request):
    return render(request,'index.html')


# attribute authority

def attributeauthority(request):
    if request.method=='POST':
        name=request.POST['Name']
        password=request.POST['Password']
        print(name,password)
        if name=='AA' and password=='AA':

            return render(request,'attributehome.html')

    return render(request,'attribute.html')

def vifi(request):
    return render(request,'vifi.html')

def vireq(request):
    data=dataownerreg.objects.all()
    return render(request,'vireq.html',{'data':data})


def stt(request):
    sql="select * from app_attribute union select * form "
    data=pd.read_sql_query(sql,connection)
    connection.commit()
  
    return render(request,'stt.html',{'cols':data.columns,'rows':data.values.tolist()})

def update(request,Name,Email):
    sql="update app_datauserregistration set status='accepted' where status='pending' and Email='%s'"%(Email)
    cur.execute(sql)
    connection.commit()
    return redirect('reqview')

def viewdo(request):
    dc = dataownerreg.objects.filter(status='approved').values('id','Name','Email')
    return render(request,'viewdo.html',{'dc':dc})


def vidureq(request):
    data=Datauserrequest.objects.all()
    return render(request,'vidureq.html',{'data':data})


def sendkey(request,datauser,key):
    dc = Datauserregistration.objects.filter(Name=datauser)
    emails = [i.Email for i in dc]
    print(emails)
    subject = 'Private Key'
    message = f'Hi {datauser}'
    cont = 'The private key to decrypt file.'
   
    KEY=str(key)
    m1 = "This message is automatic generated so dont reply to this Mail"
    m2 = "Thanking you"
    m3 = "Regards"
    m4 = "Cloud Service Provider."
    # Email=emails[0]
    # print(Email)
    # email_from = str(settings.EMAIL_HOST_USER)
    # print(email_from)

    recipient_list = "njcomputer.com@gmail.com"
    # print(recipient_list)
    # text = message + '\n' + str(KEY) + '\n' + str(m1) + '\n' + str(m2) + '\n' + str(m3) + '\n' + str(m4)
    # print(text)
    # send_mail(subject, text, email_from, recipient_list,fail_silently=False,)
    mail_content = message + '\n' + str(KEY) + '\n' + str(m1) + '\n' + str(m2) + '\n' + str(m3) + '\n' + str(m4)
    sender_address = 'njcomputer.com@gmail.com'
    sender_pass = 'sejtfzsgtnxrllji'
    receiver_address = recipient_list
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'Hi {datauser}'
    message.attach(MIMEText(mail_content, 'plain'))
    ses = smtplib.SMTP('smtp.gmail.com', 587)
    ses.starttls()
    ses.login(sender_address, sender_pass)
    text = message.as_string()
    ses.sendmail(sender_address, receiver_address, text)
    ses.quit()
    messages.info(request,'Key sent to consumer')
    return redirect("vidureq")



# def valdata(request,Datauser,filename):
#     sql="select privatekey from app_uploadfile where Datauser=%s and filename=%s"
#     val=(Datauser,filename)
#     cur.execute(sql,val)
#     content=cur.fetchone()
#
#     connection.commit()
#     print('-----------')
#     sql="update app_cloudserviceprovider set primarykey=%s where filename=%s and Datauser=%s "
#     val=(content,filename,Datauser)
#     cur.execute(sql,val)
#     connection.commit()
#     print('=================')
#     sql="insert into app_datauser_values(filename,Datauser,pri)values(%s,%s,%s)"
#     val=(filename,Datauser,content)
#     cur.execute(sql,val)
#     connection.commit()
#     print('111111111111111111')
#     sql="select * from app_datauserregistration where Name='%s'"%(Datauser)
#     cur.execute(sql)
#     a=cur.fetchone()
#     connection.commit()
#
#     subject = 'Private Key'
#     message = f'Hi {Datauser}'
#     cont = 'The private key to decrypt file.'
#     print(content)
#     print(content[0])
#     KEY=str(content[0])
#     m1 = "This message is automatic generated so dont reply to this Mail"
#     m2 = "Thanking you"
#     m3 = "Regards"
#     m4 = "Cloud Service Provider."
#     Email=a[2]
#     print(KEY)
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [Email]
#     text = message + '\n' + KEY + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
#     # send_mail(subject, text, email_from, recipient_list,fail_silently=False,)
#     sql="update app_datauser_values set status='accepted' where status='pending' and filename='%s'"%(filename)
#     cur.execute(sql)
#     connection.commit()
#     messages.info(request,'request sent to Data Consumer ')
#     return redirect('vireq')


def aalogout(request):
    return render(request,'index.html')
#
# session["dcb"]="No Request Recieved"
# dd = 'document.txt'
# f = open(dd, "r")
# data = f.read()
# sql="insert into filesupload (owneremail,FileName,Keywords,Files) values (%s,%s,%s,AES_ENCRYPT(%s,'rupesh'))"
# values=(session["nj"],FileName,Keywords,data)
# cursor.execute(sql,values)
# db.commit()