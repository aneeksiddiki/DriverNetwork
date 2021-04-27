from django.contrib import admin
from .models import Car,Customer,RenterNetwork,RideShare, CustomerNetwork,MemberInfo,Renter,RideRequest,Payments,Customergig, Gigride,EmailConfirm, CarInterest, Notification, InviteJoin
# Register your models here.
admin.site.register(Car)
admin.site.register(Customer)
admin.site.register(MemberInfo)
admin.site.register(Renter)
admin.site.register(RideRequest)
admin.site.register(Payments)
admin.site.register(Customergig)
admin.site.register(Gigride)
admin.site.register(EmailConfirm)
admin.site.register(CarInterest)
admin.site.register(Notification)
admin.site.register(RenterNetwork)
admin.site.register(CustomerNetwork)
admin.site.register(InviteJoin)
admin.site.register(RideShare)

