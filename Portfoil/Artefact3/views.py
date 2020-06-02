from django.shortcuts import render
from django.http import HttpResponse
from carRental.models import Customer
from carRental.models import Order
from carRental.models import Car
from django.shortcuts import render_to_response
from carRental.models import CustomerRegister
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    return render(request, 'carRental/index.html')

def userlogin(request):
    if request.method == "POST":
        phoneNumber = request.POST.get("phoneNumber")
        password = request.POST.get("userpw")
        user = authenticate(username=phoneNumber, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if (user.is_staff):
                    return (HttpResponseRedirect('/carRental/orderoverview'))
                else:
                    return (HttpResponseRedirect('/carRental/freebrowsing'))
            else:
                return  HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(phoneNumber, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'login/userlogin.html')
    
def homepage(request):
    return render(request, 'login/homepage.html')
def signup(request):
    if request.method == "POST":
        phoneNumber = request.POST.get("phoneNumber")
        password = request.POST.get("password")
        name = request.POST.get("name")
        role = request.POST.get("role")
        register = User()
        register.username = phoneNumber
        register.password = make_password(password)
        register.first_name = name
        if (role == "staff"):
            register.is_staff = 1
        register.save()
        return HttpResponseRedirect('/carRental/userlogin')
    return render(request, 'login/signup.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userlogin'))

def about(request):
    return HttpResponse("This is about page <a href = /carRental/>Index</a>")

def search(request):
    if 'searchBox' in request.GET:
        message = 'You searched for: ' + request.GET['searchBox']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)


order = Order.objects.all()
posts = Customer.objects.all()
cars = Car.objects.all()
store = Order.objects.filter(Order_ReturnStore = "1")
store2 = Order.objects.filter(Order_ReturnStore = "2")
store3 = Order.objects.filter(Order_ReturnStore = "3")
store4 = Order.objects.filter(Order_ReturnStore = "4")

def customeroverview(request):
    return render(request, 'carRental/customeroverview.html', {'posts': posts})
	
def orderInformtaion(request):
    return render_to_response('carRental/order.html', {'order': order})

def carInformation(request):
    return render(request, 'carRental/carInformation.html',{'cars': cars})

def orderoverview(request):
    return render_to_response('carRental/orderoverview.html', {'order': order,'store': store,'store2':store2,'store3':store3,'store4':store4})

def freebrowsing(request):
    return render(request, 'carRental/freebrowsing.html')

def storerecord(request):
    return render_to_response('carRental/storerecord.html',{'store': store,'store2':store2,'store3':store3,'store4':store4})


def sortReturnStore(request):
    if request.POST.get('filter'):
        queryset = Order.objects.filter(Order_ReturnStore=request.POST['filter'])
    
