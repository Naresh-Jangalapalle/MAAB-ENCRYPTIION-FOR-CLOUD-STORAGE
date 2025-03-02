from django.db import models

class dataownerreg(models.Model):
    Name=models.CharField(max_length=100)
    Email=models.EmailField(max_length=70)
    password=models.CharField(max_length=50)
    status=models.CharField(default='pending',max_length=50)
    

class Datauserregistration(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=70)
    password = models.CharField(max_length=50)
    status=models.CharField(default='pending',max_length=50)

class attribute(models.Model):
    Email=models.CharField(max_length=100)
    filename=models.CharField(max_length=200)
    keypair=models.CharField(max_length=100)

class datauser_values(models.Model):
    filename=models.CharField(max_length=100)
    Datauser=models.CharField(max_length=100)
    pri=models.BinaryField()
    status=models.CharField(max_length=100,default="pending")

class Datauserrequest(models.Model):
    fileid = models.CharField(max_length=100)
    datauser=models.CharField(max_length=100,null=True)
    filename=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,default="pending")
    key = models.CharField(max_length=100,null=True)
    date = models.CharField(max_length=100,null=True)

class uploadfile(models.Model):
    Dataowner=models.CharField(max_length=100)
    filename=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    filepath = models.FileField(upload_to='static/files',default='null')
    ciphertext=models.TextField()
    # tag = models.TextField()
    nounce = models.TextField()


class Cloudserviceprovider(models.Model):
    filename=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    dataowner=models.CharField(max_length=50)
    datauser=models.CharField(max_length=50)


class AttributeAuthority(models.Model):
    Dataowner=models.CharField(max_length=100)
    filename=models.CharField(max_length=100)
    date=models.CharField(max_length=100)






