from django.contrib import admin
from django.db.models import Q
from django.urls import path, include
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from rentadmin.models import EmailConfirm, Renter, InviteJoin, Customer
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.SUCCESS: 'success',message_constants.ERROR: 'danger',}

def homepage(request):
    return render(request,"leaseliger/index.html");

def joinasrenter(request):
    return render(request,"leaseliger/joinasrenter.html");

def varifyemail(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_email = request.POST.get('email')
        user_type = request.POST.get('type')
        code = get_random_string(length=8)
        find = EmailConfirm.objects.filter(email=user_email).count()
        url = "http://127.0.0.1:8000/JoinAsRenter/FinalCode/"+user_email+"/"+code
        if find < 1:
            confirm = EmailConfirm()
            confirm.first_name = first_name
            confirm.last_name = last_name
            confirm.email = user_email
            confirm.user_type = user_type
            confirm.varification_code = code
            confirm.varify_url = url
            confirm.save()
            subject, from_email, to = 'LeaseLiger Email Confirmation', 'admin@leaseliger.com', request.POST.get('email')
            text_content = 'This is an important message.'
            html_content = "<p><strong>Email Confirmation Code: </strong>" + code + "<br><p>Submit this to Activate Your Account</p>" \
                                                                                    "<br>You Can Also Follow This Link To Activate<br>"+url
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            messages.success(request, "A Confirmation Code Has Been Sent You Your Email. Plese Check Your Email")
            return redirect('../ConfirmCode/'+user_email)

def confirmcode(request,email):
    return render(request,"leaseliger/varifyemail.html",{'email': email});

def confirmpost(request):
    if request.method == "POST":
        email = request.POST.get('email')
        code = request.POST.get('varify_code')
        return redirect("../FinalCode/"+email+"/"+code)

def finalconfirm(request,email,code):
        confirm = EmailConfirm.objects.get(email=email)
        if confirm.status == "Varified":
            messages.warning(request, "Code is Already Varified. Please Login")
            return redirect('userlogin')
        else:
            if code == confirm.varification_code:
                confirm.status = "Varified"
                renter = Renter()
                renter.first_name = confirm.first_name
                renter.last_name = confirm.last_name
                renter.email = email
                User.objects.create_user(
                    username=email,
                    password='1234',
                    first_name=confirm.first_name,
                    last_name=confirm.last_name,
                    email=email
                )
                user = User.objects.get(username=email)
                group = Group.objects.get(name='renter')
                user.groups.add(group)
                confirm.save()
                renter.save()
                return redirect('confirm')
            else:
                messages.warning(request, "Varification Code Doesn't Match")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def confirm(request):
    return render(request,"leaseliger/congrats.html")

def invitejoinasrenter(request):
    return render(request,"leaseliger/invitejoin.html")

def invitejoinascustomer(request):
    return render(request,"leaseliger/invitejoincustomer.html")

def invitejoinasrentercheck(request):
    if request.method == "POST":
        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        type = request.POST.get('type')
        is_invited = InviteJoin.objects.filter(invite_email=email).count()
        if is_invited:
            invited = InviteJoin.objects.get(invite_email=email)
            if invited.status == "Confirmed":
                messages.warning(request, "This Email is Already Confirmed For Renter")
                return redirect('invitejoinasrenter')
            else:
                invite = InviteJoin.objects.get(invite_email=email)
                invite.status = "Confirmed"
                renter = Renter()
                renter.first_name = firstname
                renter.last_name = lastname
                renter.email = email
                renter.join_type = "Referred"
                renter.reference = User.objects.get(email=invite.invite_by.email)
                User.objects.create_user(
                    username=email,
                    password='1234',
                    first_name=firstname,
                    last_name=lastname,
                    email=email
                )
                user = User.objects.get(username=email)
                group = Group.objects.get(name='renter')
                user.groups.add(group)
                invite.save()
                renter.save()
                subject, from_email, to = 'Renter Account Confirmation', 'admin@leaseliger.com', request.POST.get(
                    'email')
                text_content = 'This is an important message.'
                html_content = '<h3>Welcome, ' + firstname + ' ' + lastname + '</h3>' + '<p>Username: ' + request.POST.get(
                    'email') + '</><p><p>Password: 1234</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('confirm')
        else:
            messages.warning(request, "Given Email Doesn't Match With Invite Email. Try Again !!!")
            return redirect('invitejoinasrenter')


def invitejoinascustomercheck(request):
    if request.method == "POST":
        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        is_invited = InviteJoin.objects.filter(invite_email=email).count()
        if is_invited > 0:
            invited = InviteJoin.objects.get(invite_email=email)
            if invited.status == "Confirmed":
                messages.warning(request, "This Email is Already Confirmed For Member")
                return redirect('invitejoinascustomer')
            else:
                code = get_random_string(length=8)
                invite = InviteJoin.objects.get(invite_email=email)
                invite.status = "Confirmed"
                customer = Customer()
                customer.first_name = firstname
                customer.last_name = lastname
                customer.email = email
                customer.membership = "Referred"
                customer.confirmation_code = code
                customer.save()
                invite.save()
                User.objects.create_user(
                    username=request.POST.get('email'),
                    password='limo@2020',
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email')
                )
                user = User.objects.get(username=request.POST.get('email'))
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                subject, from_email, to = 'Membership Account Confirmation', 'admin@leaseliger.com', request.POST.get('email')
                text_content = 'This is an important message.'
                html_content = '<h3>Welcome, '+firstname+' '+lastname+'</h3>'+'<p>Username: ' + request.POST.get(
                    'email') + '</><p><p>Password: limo@2020</p><h4>Confirmation Code: '+code+'</h4>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('confirm')
        else:
            messages.warning(request, "Given Email Doesn't Match With Invite Email. Try Again !!!")
            return redirect('invitejoinascustomer')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage,name='landingpage'),
    path('JoinAsRenter/', joinasrenter,name='joinasrenter'),
    path('invitejoin/renter', invitejoinasrenter,name='invitejoinasrenter'),
    path('invitejoin/renter/check', invitejoinasrentercheck,name='invitejoinasrentercheck'),
    path('invitejoin/member', invitejoinascustomer,name='invitejoinascustomer'),
    path('invitejoin/member/check', invitejoinascustomercheck,name='invitejoinascustomercheck'),
    path('JoinAsRenter/Confirm/', confirm,name='confirm'),
    path('JoinAsRenter/VarifyEmail/', varifyemail,name='varifyemail'),
    path('JoinAsRenter/ConfirmCode/<str:email>', confirmcode,name='confirmcode'),
    path('JoinAsRenter/ConfirmPost/', confirmpost,name='confirmpost'),
    path('JoinAsRenter/FinalCode/<str:email>/<str:code>', finalconfirm,name='finalconfirm'),
    path('administration/', include('rentadmin.urls')),
]
