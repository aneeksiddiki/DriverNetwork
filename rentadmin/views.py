from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Car, Customer, MemberInfo,RideShare, Renter, CustomerNetwork, RenterNetwork ,RideRequest, Payments, Customergig, Gigride, CarInterest, Notification, InviteJoin
from .forms import AddCar, CreateRenter
from .decorators import allowed_users
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from time import gmtime, strftime
from decimal import Decimal
import json
from django.core.files import File
import datetime
from PIL import Image
import imagehash
from django.contrib.messages import constants as message_constants
import cv2
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}


#-----------------------------------------------------------------------------------------------------------

def notifications(notify_to,notify_from,notify_msg,notify_url="#"):
    notify = Notification()
    notify.notifyfrom = notify_from
    notify.notifyto = notify_to
    notify.messages = notify_msg
    notify.redir_url = notify_url
    notify.save()
    return HttpResponse("OK")

def markasread(request,id):
    notify = Notification.objects.get(notificationid=id)
    notify.status = "Read"
    notify.save()
    return redirect(notify.redir_url)


#-----------------------------------------------------------------------------------------------------------

def userlogin(request):
    if request.user.is_authenticated:
        gname = request.user.groups.all()[0].name
        if gname == "admin":
            messages.success(request, "Logged In !!!")
            return redirect('adminhome')
        elif gname == "customer":
            messages.success(request, "Logged In !!!")
            return redirect('customerhome')
        elif gname == "renter":
            messages.success(request, "Logged In !!!")
            return redirect('renterhome')
        else:
            messages.info(request, 'Usernmane or Password Incorrect')
            return redirect('userlogin')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                gname = user.groups.all()[0].name
                if gname == "admin":
                    messages.success(request, "Logged In !!!")
                    return redirect('adminhome')
                elif gname == "customer":
                    messages.success(request, "Logged In !!!")
                    return redirect('customerhome')
                elif gname == "renter":
                    messages.success(request, "Logged In !!!")
                    return redirect('renterhome')
                else:
                    messages.info(request, 'Usernmane or Password Incorrect')
                    return redirect('userlogin')
            else:
                messages.info(request,'Usernmane or Password Incorrect')
                return redirect('userlogin')
        return render(request,"leaseliger/login.html")

def logoutuser(request):
    logout(request)
    return redirect('userlogin')

# def joinasrenter(request):
#     return HttpResponse("OK")

# ----------------------------------- Admin Views -------------------------------------------
@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def home(request):
    customers = Customer.objects.all()
    total_customer = customers.count()
    cars = Car.objects.all()
    total_cars = cars.count()
    #notifications(notify_from=request.user,notify_to=request.user,notify_msg="Testing",notify_url='payrequests')
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    context = {'cars': cars, 'total_customer': total_customer, 'total_cars': total_cars,'notify': notify}
    return render(request, "rentadmin/home.html", context)

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def cardetails(request, id):
    car = Car.objects.filter(carid=id).first()
    return render(request, "rentadmin/cardetails.html", {'car': car})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def addcar(request):
    form = AddCar()
    if request.method == 'POST':
        form = AddCar(request.POST)
        if form.is_valid():
            form.save()
            success = "Car Added Successfully"
            return redirect('addcar')
    return render(request, "rentadmin/addcar.html", {'form': form})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def updatecar(request, id):
    car = Car.objects.get(carid=id)
    form = AddCar(instance=car)
    if request.method == "POST":
        form = AddCar(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('../car/' + id)
    return render(request, "rentadmin/updatecar.html", {'form': form, 'carid': id})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def deletecar(request, id):
    car = Car.objects.get(carid=id)
    car.delete()
    success = "--------- Car Deleted Succesfully ---------"
    return redirect('adminhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def customerlist(request):
    customers = Customer.objects.all()
    return render(request,"rentadmin/customers.html",{'customer':customers})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def customerdetails(request,id):
    customers = Customer.objects.get(customerid=id)
    return render(request,"rentadmin/applicantdetails.html",{'customer':customers})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def createuser(request):
    form = CreateRenter()
    if request.method == "POST":
        form = CreateRenter(request.POST)
        if form.is_valid():
            form.save()
            User.objects.create_user(
                username=request.POST.get('email'),
                password='limo@2020',
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email')
            )
            user = User.objects.get(username=request.POST.get('email'))
            group = Group.objects.get(name='renter')
            user.groups.add(group)
            messages.success(request, "New Renter Added")
            return redirect('adminhome')
    return render(request, "rentadmin/createuser.html",{'form':form})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def userprofile(request):
    return render(request,"rentadmin/profile.html")

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def new_payments(request):
    payment = Payments.objects.filter(status="Pending")
    return render(request,"rentadmin/newpayment.html",{'payment': payment})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def accept_payment(request,id):
    payment = Payments.objects.get(paymentid=id)
    if payment.paid_for == "Gig Ride":
        payment.status = "Accepted"
        gigride = Gigride.objects.get(gig=payment.gig)
        gigride.status = "Accepted"
        gigride.accept_date = datetime.date.today()
        gigride.save()
        payment.save()
        customer = User.objects.get(email=gigride.gig.cid.email)
        notifications(notify_from=request.user, notify_to=customer, notify_msg="Payment Accepted For Gig Ride", notify_url='customerhome')
        messages.success(request, "Payment Accepted")
        return redirect('payrequests')
    elif payment.paid_for == "Car Reservation":
        renter = Renter.objects.get(renterid=payment.payerid)
        car = payment.car
        renter.assigned_car = car
        car.status = "Assigned"
        renter.save()
        car.save()
        payment.status = "Accepted"
        payment.save()
        messages.success(request, "Payment Accepted And "+str(car)+" Assigned To "+str(renter))
        return redirect('payrequests')
    else:
        userinfo = User.objects.get(id=payment.payerid)
        customerinfo = Customer.objects.get(email=userinfo.email)
        member = MemberInfo.objects.get(cid=customerinfo)
        prevmiles = member.miles
        member.miles = int(payment.pay_plan) + prevmiles
        member.save()
        payment.status = "Accepted"
        payment.save()
        notifications(notify_from=request.user, notify_to=userinfo, notify_msg="Payment Accepted For Miles Purchase",
                      notify_url='customerhome')
        messages.success(request, "Payment Accepted")
        return redirect('payrequests')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def imagecheck(request):
    return render(request, "rentadmin/imagecheck.html")

def compare_image(self):
    image_1 = cv2.imread(self.image_1_path, 0)
    image_2 = cv2.imread(self.image_2_path, 0)
    commutative_image_diff = self.get_image_difference(image_1, image_2)
    if commutative_image_diff < self.minimum_commutative_image_diff:
        print("Matched")
        return commutative_image_diff
    return 10000

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def imagetest(request):
    if request.method == "POST":
        return HttpResponse('OK')

def get_image_difference(i1, i2):
    image_1 = cv2.imread(i1, 0)
    image_2 = cv2.imread(i2, 0)
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['admin'])
def imagetest(request):
    if request.method == "POST":
        image_1 = cv2.imread('D:/Python Apps/Django/leaseliger/static/temp/colombia.jpg',0)
        image_2 = cv2.imread('D:/Python Apps/Django/leaseliger/static/temp/harry.jpg',0)
        first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
        second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])
        img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
        img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
        img_template_diff = 1 - img_template_probability_match

        commutative_image_diff = (img_hist_diff / 50) + img_template_diff
        return HttpResponse(commutative_image_diff)
        # img1 = request.FILES.get('checkimg_1')
        # img2 = request.FILES.get('checkimg_2')
        # hash0 = imagehash.average_hash(Image.open(img1))
        # hash1 = imagehash.average_hash(Image.open(img2))
        # n = hash0 - hash1
        # if n < 5:
        #     messages.success(request, "Images are same")
        # else:
        #     messages.success(request, "Not the same images")
        # return redirect('imagecheck')

# ----------------------------------- Landing Page Views -------------------------------------------
def membersignup(request):
    if request.method == "POST":
        code = get_random_string(length=8)
        customer = Customer()
        customer.first_name = request.POST.get('firstname')
        customer.last_name = request.POST.get('lastname')
        customer.email = request.POST.get('email')
        customer.state = request.POST.get('state')
        customer.zip = request.POST.get('zip')
        customer.city = request.POST.get('city')
        customer.phone = request.POST.get('phone')
        customer.skype = request.POST.get('skype')
        customer.whatsapp = request.POST.get('whatsapp')
        customer.membership = request.POST.get('membership')
        customer.confirmation_code = code
        customer.save()
        User.objects.create_user(
            username=request.POST.get('email'),
            password='limo@2020',
            first_name=request.POST.get('firstname'),
            last_name=request.POST.get('lastname'),
            email=request.POST.get('email')
        )
        user = User.objects.get(username=request.POST.get('email'))
        group = Group.objects.get(name='customer')
        user.groups.add(group)

        subject, from_email, to = 'Membership Email Confirmation', 'admin@leaseliger.com', request.POST.get('email')
        text_content = 'This is an important message.'
        html_content = '<p>Username: '+request.POST.get('email')+'</><p><p>Password: limo@2020</p><strong>Email Confirmation Code: </strong>' + code + '<br><p>Submit this to your Dashboard</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Membership Application Successfull. Please Check Your Email For Details. Thank You ")
        return redirect('landingpage')

def email_confirm(request):
    return HttpResponse("Hellow")

def demo(request):
    return render(request,"rentadmin/demo.html")


# ----------------------------------- customer Views -------------------------------------------
@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def customer_dashboard(request):
    usermail = request.user.email
    info = Customer.objects.filter(email=usermail).first()
    memberinfo = MemberInfo.objects.filter(cid=info.customerid).first()
    ride = RideRequest.objects.filter(Q(cid=info.customerid)).exclude(Q(status='Completed') | Q(status='Rejected')).first()
    ride_count = RideRequest.objects.filter(Q(cid=info.customerid)).exclude(Q(status='Completed') | Q(status='Rejected')).count()
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    if memberinfo:
        context = {'info': info,'memberinfo': memberinfo, 'ride': ride, 'ride_count': ride_count, 'notify': notify}
    else:
        context = {'info': info, 'ride': ride, 'ride_count': ride_count,'notify': notify}
    return render(request,"customer/customer_home.html",context)

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def customerprofile(request):
    usermail = request.user.email
    info = Customer.objects.filter(email=usermail).first()
    return render(request,"customer/profile.html",{'info':info})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def changeavatar(request):
    if request.method == "POST":
        email = request.user.email
        customer = Customer.objects.get(email=email)
        customer.avatar = request.FILES.get('avatar')
        customer.save()
        messages.success(request, "Profile Avatar Updated !!!")
        return redirect('customerprofile')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def resend_email(request):
    code = get_random_string(length=8)
    useremail = request.user.email
    customer = Customer.objects.get(email=useremail)
    customer.confirmation_code = code
    customer.save()
    subject, from_email, to = 'Membership Email Confirmation', 'admin@leaseliger.com', useremail
    text_content = 'This is an important message.'
    html_content = '<p>Username: '+useremail+'</><p><p>Password: limo@2020</p><strong>Email Confirmation Code: </strong>' + code + '<br><p>Submit this to your Dashboard</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    messages.success(request, "Verification Code Has Been Sent Again. Thank You ")
    return redirect('customerhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def verify_code(request):
    if request.method == "POST":
        code = request.POST.get('verifycode')
        useremail = request.user.email
        customer = Customer.objects.get(email=useremail)
        current_code = customer.confirmation_code
        type = customer.membership
        if current_code == code:
            ride = 0
            if type == "Silver":
                ride = 0
            elif type == "Gold":
                ride = 2
            elif type == "Platinum":
                ride = 4
            else:
                ride = 0

            member = MemberInfo()
            member.cid = customer
            member.freerides = ride
            member.membertype = type
            member.save()
            customer.status = 'Confirmed'
            customer.save()
            messages.success(request, "Email Verification Success. Enjoy Our Services")
            return redirect('customerhome')
        else:
            messages.success(request, "!!! Verification Failed. Please Check The Code Again !!!")
            return redirect('customerhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def request_ride(request,lat,lon,dstlat,dstlon,tp,ml):
    if tp == "1":
        ridetype = "General"
        useremail = request.user.email
        customer = Customer.objects.get(email=useremail)
        member = MemberInfo.objects.get(cid=customer)
        if member.miles >= int(float(ml)):
            ride = RideRequest()
            ride.cid = customer
            ride.request_type = ridetype
            ride.lat = lat
            ride.lon = lon
            ride.dstlat = dstlat
            ride.dstlon = dstlon
            ride.ridemiles = int(float(ml))
            member = MemberInfo.objects.get(cid=customer)
            if member.membertype == "Referred":
                network = CustomerNetwork.objects.get(branch_customer=customer)
                ride.customer_network_code = network.network_code
                ride.network_root = network.root_renter
            newmile = member.miles - int(float(ml))
            member.miles = newmile
            member.save()
            ride.save()
            messages.success(request, "Ride Requested. Please wait, A Chauffeur will contact you shortly")
            return redirect('customerhome')
        else:
            messages.success(request, ml+" Miles is Ride Requested. Not Enough Miles")
            return redirect('customerhome')
    elif tp == "2":
        ridetype = "Free Ride"
        useremail = request.user.email
        customer = Customer.objects.get(email=useremail)
        ride = RideRequest()
        ride.cid = customer
        ride.request_type = ridetype
        ride.lat = lat
        ride.lon = lon
        ride.ridemiles = ml
        member = MemberInfo.objects.get(cid=customer)
        if member.membertype == "Referred":
            network = CustomerNetwork.objects.get(branch_customer=customer)
            ride.customer_network_code = network.network_code
            ride.network_root = network.root_renter
        ride.save()
        messages.success(request, "Ride Requested. Please wait, A Chauffeur will contact you shortly")
        return redirect('customerhome')
    elif tp == "3":
        return HttpResponse("OK")
    else:
        messages.success(request, "Request Error !!!!")
        return redirect('customerhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def riderequest(request):
    return render(request,"customer/requestride.html")

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def customer_payment(request):
    return render(request,"customer/payment.html")

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def cashapp_payment(request):
    if request.method == "POST":
        payplan = request.POST.get('payplan')
        txnid = request.POST.get('txnid')
        paydate = request.POST.get('paydate')
        pay = Payments()
        pay.payerid = request.user.id
        pay.payer_type = "Customer"
        pay.pay_mode = "CashApp"
        pay.paid_for = "Buy Miles"
        pay.payment_date = paydate
        pay.txnid = txnid
        pay.pay_plan = payplan
        pay.save()
        admin = User.objects.get(email='aneeksiddiki@gmail.com')
        user = User.objects.get(email=request.user.email)
        notifications(admin,user,"A New Payment Submitted",'payrequests')
        messages.success(request, "Payment Submitted Succesfully")
    return redirect('customerhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def payment_history(request):
    userid = request.user.id
    payment = Payments.objects.filter(payerid=userid)
    return render(request,"customer/paymenthistory.html",{'payment': payment})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def makegig(request):
    if request.method == "POST":
        useremail = request.user.email
        customer = Customer.objects.get(email=useremail)

        if request.POST.get('stopable') == "Yes":
            stopable = "Yes"
        else:
            stopable = "No"

        if request.POST.get('nagotiable') == "Yes":
            nagotiable = "Yes"
        else:
            nagotiable = "No"

        gig = Customergig()
        gig.cid = customer
        gig.amount = request.POST.get('amount')
        gig.hours = request.POST.get('hours')
        gig.pickupdate = request.POST.get('pickupdate')
        gig.pickuptime = request.POST.get('pickuptime')
        gig.vehicletype = request.POST.get('vehicletype')
        gig.nagotiable = nagotiable
        gig.stopable = stopable
        gig.pickuploc = request.POST.get('pickuploc')
        gig.droploc = request.POST.get('droploc')
        gig.save()
        messages.success(request, "Payment Submitted Succesfully")
        return redirect('customerhome')
    else:
        messages.success(request, "Request Error")
        return redirect('customerhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def giglist(request):
    usermail = request.user.email
    customer = Customer.objects.get(email=usermail)
    gigs = Customergig.objects.filter(cid=customer)
    context = {'gigs': gigs}
    return render(request,"customer/gigboard.html",context)

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def checkrequests(request,gigid):
    gig = Customergig.objects.get(gigid=gigid)
    gigride = Gigride.objects.filter(gig=gig)
    return render(request,"customer/checkrequests.html",{'gigride': gigride})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def deletegigrequest(request):
    if request.method == "POST":
        id = request.POST.get('gigrideid')
        gigride = Gigride.objects.get(gigrideid=id)
        gigride.delete()
        messages.success(request,"Request of Gig ID# "+id+" is Deleted By Customer")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def payforgig(request):
    if request.method == "POST":
        rideid = request.POST.get('gigrideid')
        amount = request.POST.get('amount')
        txnid = request.POST.get('txnid')
        paydate = request.POST.get('paydate')
        customer = Customer.objects.get(email=request.user.email)
        cid = customer.customerid
        gigride = Gigride.objects.get(gigrideid=rideid)
        if gigride.offer_amount:
            if gigride.status == "Counter Accepted":
                if gigride.counter_amount == float(amount):
                    payment = Payments()
                    payment.payerid = cid
                    payment.pay_amount = float(amount)
                    payment.payer_type = "Customer"
                    payment.pay_mode = "CashApp"
                    payment.paid_for = "Gig Ride"
                    payment.gig = gigride.gig
                    payment.payment_date = paydate
                    payment.txnid = txnid
                    payment.save()
                    gigride.sattled_amount = gigride.counter_amount
                    gigride.sattled_hours = gigride.counter_hours
                    gigride.status = "Pending"
                    gigride.save()
                    messages.success(request, "Payment Successfully Submitted")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request,"Offered Amount Doesn't Match With Submitted Amount",extra_tags='danger')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                if gigride.offer_amount == float(amount):
                    payment = Payments()
                    payment.payerid = cid
                    payment.pay_amount = float(amount)
                    payment.payer_type = "Customer"
                    payment.pay_mode = "CashApp"
                    payment.paid_for = "Gig Ride"
                    payment.gig = gigride.gig
                    payment.payment_date = paydate
                    payment.txnid = txnid
                    payment.save()
                    gigride.sattled_amount = gigride.offer_amount
                    gigride.sattled_hours = gigride.offer_hours
                    gigride.status = "Pending"
                    gigride.save()
                    messages.success(request, "Payment Successfully Submitted")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.error(request,"Offered Amount Doesn't Match With Submitted Amount",extra_tags='danger')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            if gigride.sattled_amount == float(amount):
                selected_gig = Customergig.objects.get(gigid=gigride.gig.gigid)
                payment = Payments()
                payment.payerid = cid
                payment.pay_amount = float(amount)
                payment.payer_type = "Customer"
                payment.pay_mode = "CashApp"
                payment.paid_for = "Gig Ride"
                payment.gig = selected_gig
                payment.payment_date = paydate
                payment.txnid = txnid
                payment.save()
                gigride.status = "Pending"
                gigride.save()
                messages.success(request, "Payment Successfully Submitted")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "Sattled Amount Doesn't Match With Submitted Amount",extra_tags='danger')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def renterinfo(request,id):
    info = Renter.objects.get(renterid=id)
    return render(request,"customer/renterprofile.html",{'info': info})


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def countergigrequest(request):
    if request.method == "POST":
        rideid = request.POST.get('gigrideid')
        gigride = Gigride.objects.get(gigrideid=rideid)
        gigride.counter_hours = request.POST.get('hours')
        gigride.counter_amount = request.POST.get('amount')
        gigride.status = "Countered"
        gigride.save()
        renter = User.objects.get(email=gigride.offered_by.email)
        customer = User.objects.get(email=gigride.gig.cid.email)
        notifications(notify_to=renter,notify_from=customer,notify_msg="GigRide Offer is Countered",notify_url="gigboard")
        messages.success(request, "Counter Offer Made Successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def infocomplete(request):
    if request.method == "POST":
        skype = "N/A"
        whatsapp = "N/A"
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        if request.POST.get('skype'):
            skype = request.POST.get('skype')
        if request.POST.get('whatsapp'):
            whatsapp = request.POST.get('whatsapp')
        contact = request.POST.get('contact')
        carrier = request.POST.get('carrier')
        invite = InviteJoin.objects.get(invite_email=request.user.email)
        if state and city and zip and contact and carrier:
            customer = Customer.objects.get(email=request.user.email)
            customer.state = state
            customer.city = city
            customer.zip = zip
            customer.skype = skype
            customer.whatsapp = whatsapp
            customer.phone = contact
            customer.notify_mail = contact+'@'+carrier
            customer.reference = invite.invite_by
            customer.save()
            network = CustomerNetwork()
            network.root_renter = invite.invite_by
            network.branch_customer = customer
            network.network_code = invite.invite_by.network_code
            network.save()
            messages.warning(request, "Information Saved Successfully")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, "Please Fill All Required The Fields")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['customer'])
def testapi(request):
    if request.method == "POST":
        pickup = request.POST.get('pickup')
        destination = request.POST.get('destination')
        return HttpResponse("<h3>Pickup:</h3> "+pickup+"<br>"+"<h3>Destination:</h3> "+destination)


# ----------------------------------- Renter Views -------------------------------------------

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def renter_dashboard(request):
    info = Renter.objects.get(email=request.user.email)
    is_interested = CarInterest.objects.filter(renter=info).count()
    # with open('static/cities.json') as json_data:
    #     city = json.load(json_data)
    cars = Car.objects.filter(renter__isnull= True)
    ride_count = RideRequest.objects.filter(status='Pending',network_root=info).count()
    active_ride = RideRequest.objects.filter(Q(driver=info),~Q(status='Completed')).first()
    active_gig = Gigride.objects.filter(offered_by=info,status="Accepted")
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    try:
        networkcode = RenterNetwork.objects.get(branch_renter=info).network_code
        shared = RideShare.objects.filter(network_code=networkcode).count()
    except RenterNetwork.DoesNotExist:
        shared = 0
    return render(request,"renter/renter_home.html",{'info':info,'ride_count':ride_count,'active_ride':active_ride,'active_gig':active_gig, 'is_interested':is_interested, 'cars': cars, 'notify': notify, 'shared': shared })

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def renter_profile(request):
    info = Renter.objects.get(email=request.user.email)
    return render(request,"renter/profile.html",{'info':info})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def changerenteravatar(request):
    if request.method == "POST":
        email = request.user.email
        renter = Renter.objects.get(email=email)
        renter.avatar = request.FILES.get('avatar')
        renter.save()
        messages.success(request, "Profile Avatar Updated !!!")
        return redirect('renterprofile')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def ride_requests(request):
    me = Renter.objects.get(email=request.user.email)
    ride = RideRequest.objects.filter(~Q(status='Completed'),Q(network_root=me))
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    return render(request,"renter/riderequest.html",{'ride':ride,'notify': notify})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def accept_ride(request,id):
    useremail = request.user.email
    renter = Renter.objects.get(email=useremail)
    ride = RideRequest.objects.get(requestid=id)
    ride.status = "Accepted"
    ride.driver = renter
    ride.save()
    messages.success(request, "Accepted A Ride Request")
    return redirect('renterhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def completeride(request,id):
    riderequest = RideRequest.objects.get(requestid=id)
    point = riderequest.cid.points + Decimal(0.25)
    riderequest.cid.points = point
    miles = riderequest.ridemiles
    if riderequest.is_shared == "Yes":
        payment = round((miles/5))*5
        admincut = payment*(2/100)
        sharecut = payment*(5/100)
        amount = payment - (admincut+sharecut)
        sharedby = RideShare.objects.get(ride=riderequest).shared_by
        sharedby.balance = Decimal(sharecut) + sharedby.balance
        sharedby.points = Decimal(0.15) + sharedby.points
        sharedby.save()
        riderequest.driver.balance = Decimal(amount) + riderequest.driver.balance
        riderequest.driver.points = Decimal(0.25) + riderequest.driver.points
        riderequest.driver.save()
    else:
        payment = round((miles / 5)) * 5
        admincut = payment * (2 / 100)
        amount = payment - admincut
        riderequest.driver.balance = Decimal(amount) + riderequest.driver.balance
        riderequest.driver.points = Decimal(0.25) + riderequest.driver.points
        riderequest.driver.save()
    riderequest.status = "Completed"
    riderequest.save()
    riderequest.cid.save()
    messages.success(request, "Completed A Ride Request")
    return redirect('renterhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def gigboard(request):
    rg = {}
    ag = {}
    cg = {}
    coa = {}
    flag = "Active"
    useremail = request.user.email
    renter = Renter.objects.get(email=useremail)
    if renter.assigned_car:
        cartype = renter.assigned_car.category
        running_gig = Gigride.objects.all()
        gigs = Customergig.objects.filter(vehicletype=cartype)
        for i in running_gig:
            if i.gig in gigs and i.status == "Accepted":
                x = {i.gig.gigid: i.gig.gigid}
                ag.update(x)
            elif i.gig in gigs and i.status == "Countered":
                y = {i.gig.gigid: i.gig.gigid}
                cg.update(y)
            elif i.gig in gigs and i.status == "Counter Accepted":
                m = {i.gig.gigid: i.gig.gigid}
                coa.update(m)
            else:
                z = {i.gig.gigid: i.gig.gigid}
                rg.update(z)
        notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
        return render(request,"renter/giglist.html",{'gigs': gigs, 'rg': rg,'ag': ag,'cg': cg,'coa': coa,'flag': flag,'notify':notify})
    else:
        flag = "Pending"
        notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
        return render(request, "renter/giglist.html", {'flag': flag,'notify':notify})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def gigrequest(request,id):
    cgig = Customergig.objects.get(gigid=id)
    useremail = request.user.email
    renter = Renter.objects.get(email=useremail)
    gigride = Gigride()
    gigride.gig = cgig
    gigride.offered_by = renter
    gigride.sattled_amount = cgig.amount
    gigride.sattled_hours = cgig.hours
    gigride.save()
    customer = User.objects.get(email=cgig.cid.email)
    notifications(notify_to=customer, notify_from=request.user, notify_msg="A GigRide Request is Placed",
                  notify_url="giglist")
    messages.success(request, "Gig Request Successfull")
    return redirect('renterhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def gigoffer(request):
    if request.method == "POST":
        offer_amount = request.POST.get('offer_amount')
        offer_hour = request.POST.get('offer_hour')
        id = request.POST.get('gigid')
        cgig = Customergig.objects.get(gigid=id)
        useremail = request.user.email
        renter = Renter.objects.get(email=useremail)
        gigride = Gigride()
        gigride.gig = cgig
        gigride.offered_by = renter
        gigride.offer_amount = offer_amount
        gigride.offer_hours = offer_hour
        gigride.status = "Offered"
        gigride.save()
        customer = User.objects.get(email=cgig.cid.email)
        notifications(notify_to=customer, notify_from=request.user, notify_msg="A GigRide Offer is Placed",
                      notify_url="giglist")
        messages.success(request, "Gig Offer Successfull")
        return redirect('renterhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def savepersonalinfo(request):
    if request.method == "POST":
        useremail = request.user.email
        renter = Renter.objects.get(email=useremail)
        renter.state = request.POST.get('state')
        renter.city = request.POST.get('city')
        renter.zip = request.POST.get('zip')
        renter.phone = request.POST.get('contact')
        renter.experience = request.POST.get('experience')
        if request.POST.get('skype'):
            renter.skype = request.POST.get('skype')
        if request.POST.get('whatsapp'):
            renter.whatsapp = request.POST.get('whatsapp')
        renter.contact = request.POST.get('contact')
        renter.notify_mail = request.POST.get('contact')+"@"+request.POST.get('carrier')
        renter.save()
        messages.success(request, "Personal Information Saved Successfully")
        return redirect('renterhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def savedriverinfo(request):
    if request.method == "POST":
        net_code = strftime("%H%M%m%Y%d%S", gmtime())
        useremail = request.user.email
        renter = Renter.objects.get(email=useremail)
        renter.driving_license = request.POST.get('license_no')
        renter.license_image = request.FILES.get('license_image')
        renter.chauffeur = request.POST.get('chauffeur')
        renter.licenseinyears = request.POST.get('licenseinyears')
        renter.drivinghistory = request.POST.get('drivinghistory')
        renter.currentjob = request.POST.get('currentjob')
        renter.workedincar = request.POST.get('workedincar')
        renter.caraccident = request.POST.get('caraccident')
        renter.carprefer = request.POST.get('carprefer')
        renter.qualityodriver = request.POST.get('qualityodriver')
        renter.network_code = net_code
        if request.POST.get('insurance_no'):
            renter.insurance_no = request.POST.get('insurance_no')
        if request.FILES.get('insurance_image'):
            renter.insurance_image = request.FILES.get('insurance_image')
        renter.status = "Active"
        if renter.join_type == "Referred":
            root = InviteJoin.objects.get(invite_email=useremail).invite_by
            network = RenterNetwork()
            network.root_renter = root
            network.network_code = root.network_code
            network.branch_renter = renter
            network.save()
        renter.save()
        messages.success(request, "Driving Information Saved Successfully")
        return redirect('renterhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def rentercardetails(request, carid):
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    car = Car.objects.get(carid=carid)
    return render(request, "renter/cardetails.html", {'car': car, 'notify': notify})


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def generalinterest(request, carid):
    car = Car.objects.filter(carid=carid).first()
    renter = Renter.objects.get(email=request.user.email)
    interest = CarInterest()
    interest.car = car
    interest.renter = renter
    interest.interest_type = "General"
    interest.save()
    messages.success(request,"Car Interest For "+str(car)+" Submitted Successfully")
    return redirect('renterhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def carreserve(request,carid):
    if request.method == "POST":
        car = Car.objects.get(carid=carid)
        renter = Renter.objects.get(email=request.user.email)
        rid = renter.renterid
        payment = Payments()
        payment.payerid = rid
        payment.pay_amount = request.POST.get('amount')
        payment.payer_type = "Renter"
        payment.pay_mode = "CashApp"
        payment.paid_for = "Car Reservation"
        payment.car = car
        payment.payment_date = request.POST.get('paydate')
        payment.txnid = request.POST.get('txnid')
        interest = CarInterest()
        interest.car = car
        interest.renter = renter
        interest.interest_type = "Reserve"
        interest.deposit_amount = request.POST.get('amount')
        interest.save()
        payment.save()
        messages.success(request,str(car)+" is Reserved For You. Admin Will Confirm Your Payment")
        return redirect('renterhome')

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def counteroffers(request,id):
    gigs = Customergig.objects.get(gigid=id)
    gigride = Gigride.objects.get(gig = gigs)
    if gigride.status == "Countered":
        notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
        return render(request,"renter/counterinfo.html",{'gigride': gigride, 'notify':notify})
    else:
        messages.warning(request, "Gig Ride is No Longer Countered")
        return redirect('gigboard')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def rejectgigride(request):
    if request.method == "POST":
        id = request.POST.get('rideid')
        gigride = Gigride.objects.get(gigrideid=id)
        gigride.delete()
        customer = User.objects.get(email=gigride.gig.cid.email)
        notifications(notify_from=request.user,notify_to=customer,notify_msg="A Gig Request Has Been Rejected",notify_url="giglist")
        messages.warning(request, "Gig Ride Request Rejected")
        return redirect('gigboard')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def acceptcounteroffer(request):
    if request.method == "POST":
        id = request.POST.get('rideid')
        gigride = Gigride.objects.get(gigrideid=id)
        gigride.status = "Counter Accepted"
        gigride.save()
        customer = User.objects.get(email=gigride.gig.cid.email)
        notifications(notify_from=request.user, notify_to=customer, notify_msg="A Gig Counter Has Been Accepted",
                      notify_url="giglist")
        messages.success(request, "Gig Ride Counter Request Accepted")
        return redirect('gigboard')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def runninggig(request):
    info = Renter.objects.get(email=request.user.email)
    active_gig = Gigride.objects.filter(offered_by=info, status="Accepted")
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    return render(request,"renter/runninggig.html",{'gigs': active_gig,'notify': notify})


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def networkhome(request):
    me = Renter.objects.get(email=request.user.email)
    rentercount = RenterNetwork.objects.filter(root_renter=me).count()
    customercount = CustomerNetwork.objects.filter(root_renter=me).count()
    return render(request,"renter/network_dashboard.html",{'rentercount': rentercount, 'customercount': customercount})

@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def invitedriver(request):
    if request.method == "POST":
        fullname = request.user.first_name+" "+request.user.last_name
        useremail = request.POST.get('email')
        link = "http://127.0.0.1:8000/invitejoin/renter"
        renter = Renter.objects.get(email=request.user.email)
        invite = InviteJoin()
        invite.invite_by = renter
        invite.invite_email = request.POST.get('email')
        invite.invite_type = "Renter"
        invite.save()
        emailtext = render_to_string('renter/emailinvite.html', {'fullname': fullname,'link': link})
        subject, from_email, to = 'Membership Email Confirmation', 'admin@leaseliger.com', useremail
        text_content = 'This is an important message.'
        html_content = emailtext
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Driver Invite to "+useremail+" is successfull")
        return redirect('renterhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def invitecustomer(request):
    if request.method == "POST":
        fullname = request.user.first_name+" "+request.user.last_name
        useremail = request.POST.get('email')
        link = "http://127.0.0.1:8000/invitejoin/member"
        renter = Renter.objects.get(email=request.user.email)
        invite = InviteJoin()
        invite.invite_by = renter
        invite.invite_email = request.POST.get('email')
        invite.invite_type = "Customer"
        invite.save()
        emailtext = render_to_string('renter/emailinvitecustomer.html', {'fullname': fullname,'link': link})
        subject, from_email, to = 'Membership Email Confirmation', 'admin@leaseliger.com', useremail
        text_content = 'This is an important message.'
        html_content = emailtext
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, "Customer Invite to "+useremail+" is successfull")
        return redirect('renterhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def networkrenterlist(request):
    me = Renter.objects.get(email=request.user.email)
    renters = RenterNetwork.objects.filter(root_renter=me)
    return render(request, "renter/network_renters.html", {'renters': renters})


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def shareride(request,rideid):
    ridereq = RideRequest.objects.get(requestid=rideid)
    renter = Renter.objects.get(email=request.user.email)
    share = RideShare()
    share.network_code = renter.network_code
    share.ride = ridereq
    share.shared_by = renter
    share.save()
    ridereq.status = 'Shared'
    ridereq.save()
    messages.success(request, "Ride Shared Among Network Successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def rideshared(request):
    me = Renter.objects.get(email=request.user.email)
    ride = RideShare.objects.filter(~Q(shared_by=me))
    notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
    return render(request, "renter\sharedrides.html",{'notify': notify,'ride': ride})


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def acceptsharedride(request,shareid):
    useremail = request.user.email
    renter = Renter.objects.get(email=useremail)
    share = RideShare.objects.get(shareid=shareid)
    share.ride.status = "Accepted"
    share.ride.driver = renter
    share.ride.is_shared = "Yes"
    share.ride.save()
    share.accepted_by = renter
    share.status = "Accepted"
    share.save()
    messages.success(request, "Accepted A Ride Request")
    return redirect('renterhome')


@login_required(login_url='userlogin')
@allowed_users(allowed_roles=['renter'])
def addowncar(request):
    if request.method == "POST":
        carimage = request.FILES.get('carimage')
        vinno = request.POST.get('vinno')
        category = request.POST.get('category')
        make = request.POST.get('make')
        model = request.POST.get('model')
        mfgyear = request.POST.get('mfgyear')
        insuarance_image = request.FILES.get('insuarance_image')
        car = Car()
        car.primary_image = carimage
        car.vin = vinno
        car.category = category
        car.make = make
        car.model = model
        car.mfg_year = mfgyear
        car.insurance_image = insuarance_image
        car.status = "Assigned"
        car.save()
        my_car = Car.objects.get(vin=vinno)
        renter = Renter.objects.get(email=request.user.email)
        renter.insurance_image = insuarance_image
        renter.assigned_car = my_car
        renter.save()
        messages.success(request, "Car Added and Assigned Successfully")
        return redirect('renterhome')

# @login_required(login_url='userlogin')
# @allowed_users(allowed_roles=['renter'])
# def rentercardetails(request,carid):
#     notify = Notification.objects.filter(notifyto=request.user).exclude(status="Read")
#     car = Car.objects.get(carid=carid)
#     return render(request,"renter/cardetails.html",{ "notify": notify, "car": car })
