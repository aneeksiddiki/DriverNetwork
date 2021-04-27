from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
class Car(models.Model):
    CATEGORY = (
        ('SUV', 'SUV'),
        ('SEDAN', 'SEDAN'),
        ('SPORTS CAR', 'SPORTS CAR'),
        ('STATION WAGON', 'STATION WAGON'),
        ('HATCHBACK', 'HATCHBACK'),
        ('CONVERTIBLE', 'CONVERTIBLE'),
        ('MINIVAN', 'MINIVAN'),
        ('PICKUP TRUCK', 'PICKUP TRUCK'),
    )
    carid = models.AutoField(primary_key=True)
    make = models.CharField(max_length=200)
    vin = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    mfg_year = models.IntegerField()
    category = models.CharField(max_length=200, choices=CATEGORY)
    primary_image = models.ImageField(upload_to="cars",default='none.jpg')
    insurance_image = models.ImageField(upload_to="cars",default='none.jpg')
    status = models.CharField(max_length=100,default="Unassigned")
    owner = models.CharField(max_length=100,default="Company")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.make + " " + self.model+" "+str(self.mfg_year)


class EmailConfirm(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=200)
    varification_code = models.CharField(max_length=200)
    varify_url = models.TextField()
    status = models.CharField(max_length=200,default='Pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name+" - "+self.status

class Renter(models.Model):
    OPTION = (
        ('Yes','Yes'),
        ('No','No'),
    )
    renterid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(null=True,unique=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    notify_mail = models.EmailField(null=True)
    skype = models.CharField(max_length=200, default="N/A")
    whatsapp = models.CharField(max_length=200, default="N/A")
    experience = models.CharField(max_length=200, null=True)
    driving_license = models.CharField(max_length=200, default="N/A")
    license_image = models.ImageField(upload_to="renters", default="no-one.jpg")
    chauffeur = models.CharField(max_length=200,choices=OPTION,default="No")
    licenseinyears = models.IntegerField(null=True)
    drivinghistory = models.CharField(max_length=200,null=True)
    currentjob = models.CharField(max_length=200,null=True)
    workedincar = models.CharField(max_length=200,null=True)
    caraccident = models.CharField(max_length=200,null=True)
    carprefer = models.CharField(max_length=200,null=True)
    qualityodriver = models.CharField(max_length=200,null=True)
    insurance_no = models.CharField(max_length=200,null=True)
    insurance_image = models.ImageField(upload_to="renters",default="no-one.jpg")
    assigned_car = models.OneToOneField(Car, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200,null=True,default="Pending")
    avatar = models.ImageField(upload_to="renters", default="no-one.jpg")
    join_type = models.CharField(max_length=100,default="General")
    balance = models.DecimalField(decimal_places=2,max_digits=7,default=0)
    points = models.DecimalField(decimal_places=2,max_digits=7,default=0)
    reference = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    network_id = models.CharField(max_length=100,null=True)
    network_code = models.CharField(max_length=100,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Customer(models.Model):
    customerid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(null=True,unique=True)
    state = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    notify_mail = models.EmailField(null=True)
    skype = models.CharField(max_length=200, null=True, default="N/A")
    whatsapp = models.CharField(max_length=200, null=True, default="N/A")
    membership = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200,default="Pending")
    confirmation_code = models.CharField(max_length=200,null=True)
    avatar = models.ImageField(upload_to="customers",null=True, default="no-one.jpg")
    reference = models.ForeignKey(Renter, on_delete=models.SET_NULL, null=True)
    points = models.DecimalField(decimal_places=2,max_digits=7,default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class MemberInfo(models.Model):
    TYPE = (
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Referred', 'Referred'),
    )
    membershipid = models.AutoField(primary_key=True)
    cid = models.OneToOneField(Customer, on_delete=models.CASCADE)
    freerides = models.IntegerField(null=True)
    miles = models.IntegerField(default=0)
    membertype = models.CharField(max_length=200,choices=TYPE,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.cid)+" - "+self.membertype

class Customergig(models.Model):
    gigid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2,max_digits=7)
    hours = models.IntegerField()
    pickupdate = models.DateField()
    pickuptime = models.TimeField()
    vehicletype = models.CharField(max_length=200)
    nagotiable = models.CharField(max_length=200)
    stopable = models.CharField(max_length=200)
    pickuploc = models.CharField(max_length=200)
    droploc = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default="Active")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.cid)+" - "+str(self.amount)+" - "+str(self.pickupdate)

class Gigride(models.Model):
    gigrideid = models.AutoField(primary_key=True)
    gig = models.ForeignKey(Customergig, on_delete=models.SET_NULL,null=True)
    offered_by = models.ForeignKey(Renter, on_delete=models.SET_NULL,null=True)
    offer_amount = models.DecimalField(null=True,decimal_places=2,max_digits=7)
    offer_hours = models.IntegerField(null=True)
    counter_hours = models.IntegerField(null=True)
    counter_amount = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    sattled_amount = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    sattled_hours = models.IntegerField(null=True)
    status = models.CharField(max_length=200,default='Requested')
    accept_date = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.gig)+" - "+str(self.date_created)+" - "+str(self.status)

class RideRequest(models.Model):
    OPT = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    requestid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    request_type = models.CharField(max_length=200,default="General")
    lat = models.CharField(max_length=200,null=True)
    lon = models.CharField(max_length=200,null=True)
    dstlat = models.CharField(max_length=200, null=True)
    dstlon = models.CharField(max_length=200, null=True)
    ridemiles = models.IntegerField(null=True)
    status = models.CharField(max_length=200,default="Pending")
    gig = models.CharField(max_length=200,default="0")
    driver = models.ForeignKey(Renter,on_delete=models.SET_NULL,null=True, related_name='ride_driver')
    customer_network_code = models.CharField(max_length=100,null=True)
    network_root = models.ForeignKey(Renter, on_delete=models.SET_NULL, null=True, related_name='network_root')
    is_shared = models.CharField(max_length=100,default="No",choices=OPT)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.request_type+" - "+str(self.cid)+" At: "+str(self.date_created)

class Payments(models.Model):
    MODE = (
        ('CashApp', 'CashApp'),
        ('PayPal', 'PayPal'),
        ('Card', 'Card'),
    )
    PAYER = (
        ('Customer', 'Customer'),
        ('Renter', 'Renter'),
    )
    PAYFOR = (
        ('Weekly Payment', 'Weekly Payment'),
        ('Buy Miles', 'Buy Miles'),
        ('Gig Ride', 'Gig Ride'),
        ('Car Reservation', 'Car Reservation'),
    )
    PLAN = (
        ('5', '5 Miles - 5 USD'),
        ('10', '10 Miles - 10 USD'),
        ('15', '15 Miles - 15 USD'),
        ('20', '20 Miles - 20 USD'),
    )
    paymentid = models.AutoField(primary_key=True)
    payerid = models.IntegerField()
    pay_plan = models.CharField(max_length=200,choices=PLAN,null=True)
    pay_amount = models.DecimalField(null=True,decimal_places=2,max_digits=7)
    payer_type = models.CharField(max_length=200,choices=PAYER)
    pay_mode = models.CharField(max_length=200,choices=MODE)
    paid_for = models.CharField(max_length=200,choices=PAYFOR)
    gig = models.ForeignKey(Customergig, on_delete=models.SET_NULL,null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL,null=True)
    payment_date = models.DateField()
    txnid = models.CharField(max_length=200,default="N/A")
    status = models.CharField(max_length=200,default="Pending")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.payerid)+" - "+str(self.payer_type)+" - "+str(self.paid_for)

class CarInterest(models.Model):
    TYPE = (
        ('General', 'General'),
        ('Reserve', 'Reserve'),
    )
    interestid = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car,on_delete=models.SET_NULL,null=True)
    renter = models.ForeignKey(Renter,on_delete=models.SET_NULL,null=True)
    interest_type = models.CharField(max_length=200,null=True,choices=TYPE)
    deposit_amount = models.CharField(max_length=200,null=True)
    status = models.CharField(max_length=200,default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.car)+" - "+str(self.renter)+" - "+str(self.interest_type)

class InviteJoin(models.Model):
    INVITETYPE = (
        ('Customer', 'Customer'),
        ('Renter', 'Renter'),
    )
    inviteid = models.AutoField(primary_key=True)
    invite_by = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True)
    invite_email = models.EmailField(null=True)
    status = models.CharField(max_length=100, default="Pending")
    invite_type = models.CharField(max_length=100, choices=INVITETYPE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.inviteid) + " - " + str(self.invite_by)+ " - " + str(self.invite_email)+ " - " + str(self.status)

class RenterNetwork(models.Model):
    networkid = models.AutoField(primary_key=True)
    network_code = models.CharField(max_length=100, null=True)
    root_renter = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True, related_name='root_renter')
    branch_renter = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True, related_name='branch_renter')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.networkid)+" - "+str(self.root_renter)+" - "+str(self.branch_renter)

class CustomerNetwork(models.Model):
    networkid = models.AutoField(primary_key=True)
    network_code = models.CharField(max_length=100,null=True)
    root_renter = models.ForeignKey(Renter, on_delete=models.CASCADE, null=True)
    branch_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.networkid)+" - "+str(self.root_renter)+" - "+str(self.branch_customer)

class RideShare(models.Model):
    shareid = models.AutoField(primary_key=True)
    network_code = models.CharField(max_length=100,null=True)
    ride = models.ForeignKey(RideRequest, on_delete=models.SET_NULL, null=True)
    shared_by = models.ForeignKey(Renter, on_delete=models.SET_NULL, null=True, related_name='shared_by')
    accepted_by = models.ForeignKey(Renter, on_delete=models.SET_NULL, null=True, related_name='accepted_by')
    status = models.CharField(max_length=100,default='Pending')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.shareid)+' - '+str(self.network_code)+" - "+str(self.shared_by)+" - "+str(self.status)


class Notification(models.Model):
    OPT = (
        ('Read', 'Read'),
        ('Unread', 'Unread'),
    )
    notificationid = models.AutoField(primary_key=True)
    notifyto = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='notify_to_set')
    notifyfrom = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='notify_from_set')
    messages = models.CharField(max_length=200,null=True)
    redir_url = models.TextField(null=True)
    status = models.CharField(max_length=200,choices=OPT,default="Unread")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "ID: "+str(self.notificationid)+" -: "+str(self.notifyfrom)+" -> "+str(self.notifyto)+" :- "+str(self.messages)