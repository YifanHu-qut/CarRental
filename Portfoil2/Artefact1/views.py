from django.shortcuts import render
from django.http import HttpResponse
from carRental.models import Order
from carRental.models import StaffInformation
from carRental.models import someStoreMonthly
from django.shortcuts import render_to_response
from carRental.models import CustomerRegister
from carRental.models import StaffInformation
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Count
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    return render(request, 'carRental/index.html')

def userlogin(request):
    if request.method == "POST":
        userName = request.POST.get("username")
        password = request.POST.get("userpw")
        user = authenticate(username=userName, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if (user.is_staff):
                    return (HttpResponseRedirect('/carRental/orderoverview'))
                else:
                    return (HttpResponseRedirect('/carRental/freebrowsing'))
            else:
                return  HttpResponse("Your account is disabled.")
        else:
            error_msg = "Invalid PhoneNumber or password!"
            return render(request, 'login/userlogin.html',{'error_msg':error_msg})

    else:
        return render(request, 'login/userlogin.html')
    
def homepage(request):
    return render(request, 'login/homepage.html')
def signup(request):
    if request.method == "POST":
        userName = request.POST.get("username")
        exist = User.objects.filter(username = userName)
        if (len(exist) == 0):
            phoneNumber = request.POST.get("phoneNumber")
            password = request.POST.get("password")
            name = request.POST.get("name")
            role = request.POST.get("role")
            gender = request.POST.get("gender")
            dirth = request.POST.get("DOB")
            occupation =request.POST.get("occupation")
            address =request.POST.get("streetAddress")
            register = User()
            register.username = userName
            register.password = make_password(password)
            register.last_name = name
            if (role == "staff"):
                register.is_staff = 1 
                staffInfor = StaffInformation()
                staffInfor.Name = name
                staffInfor.PhoneNumber=userName
                staffInfor.Gender = gender
                staffInfor.Address = address
                staffInfor.save()
            else:
                informationRecord = CustomerRegister()
                informationRecord.Name = name
                informationRecord.PhoneNumber=phoneNumber
                informationRecord.Gender = gender
                informationRecord.Dirth = dirth
                informationRecord.Occupation = occupation
                informationRecord.Address = address
                informationRecord.save()
            register.save()
            return HttpResponseRedirect('/carRental/userlogin')
        else:
            error_msg = "Username existed!"
            return render(request, 'login/signup.html',{'error_msg':error_msg})
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

#Used to sign the object to variable
order = Order.objects.all().order_by('Order_ID')
storeGroup = Order.objects.all().order_by('Order_PickupStore')
def monthlyoutcome(request):
    if 'store' in request.GET:
        store = request.GET.get("store")
    if 'year' in request.GET:
        year = request.GET.get("year")
        month = request.GET.get("month")
        carID = []
        carnumber = []
        carname = []
        Store_ID = []
        Store_address = []
        Car_BodyType = []
        if(store == ""):
            monthoutcome = someStoreMonthly.objects.filter(Pickup_Or_Return_Date__istartswith = year + month).order_by('Car_MakeName')
            orderedByCar = monthoutcome.values_list('Car_ID', 'Car_MakeName','Store_ID','Store_address','Car_BodyType').annotate(total_car = Count('Car_ID')).order_by('Car_ID')
            for i in range(len(orderedByCar)):
                for a in range(0,len(orderedByCar[i]),6):
                    carID.append(orderedByCar[i][a])
                for b in range(4,len(orderedByCar[i]),6):
                    carnumber.append(orderedByCar[i][b])
                for c in range(1,len(orderedByCar[i]),6):
                    carname.append(orderedByCar[i][c])
                for d in range(2,len(orderedByCar[i]),6):
                    Store_ID.append(orderedByCar[i][d])
                for e in range(3,len(orderedByCar[i]),6):
                    Store_address.append(orderedByCar[i][e])
                for f in range(5,len(orderedByCar[i]),6):
                    Car_BodyType.append(orderedByCar[i][f])
        monthCount = monthoutcome.count()
        monthCount = [monthCount]
        year = [year]
        month = [month]
        totalList = zip(carID, carnumber, carname,Store_ID,Store_address,Car_BodyType)
        if len(monthoutcome) == 0:
            error_msg = "There is no order this month"
            return render(request, 'carRental/monthlyOutcome.html',{'error_msg':error_msg})
        return render(request, 'carRental/monthlyOutcome.html', {'monthoutcome': monthoutcome, 'monthCount': monthCount, 'year': year, 'month': month, 'carOutcome':totalList})       
    return render(request, 'carRental/monthlyOutcome.html')  

def customeroverview(request):
    return render(request, 'carRental/customeroverview.html', {'order': order})
	
def orderInformtaion(request):
    return render_to_response('carRental/order.html', {'order': order})

def caroverview(request):
    return render(request, 'carRental/caroverview.html',{'order': order})

def orderoverview(request):
    error_msg=""
    staffInfor = StaffInformation.objects.all()
    if request.method == "POST":
        orderID = request.POST.get("orderID")
        orderCreateDate = request.POST.get("orderCreateDate")
        orderPickupDate = request.POST.get("orderPickupDate")
        orderPickupStore = request.POST.get("orderPickupStore")
        orderReturnDate = request.POST.get("orderReturnDate")
        orderReturnStore = request.POST.get("orderReturnStore")
        customerID = request.POST.get("customerID")
        customerName =request.POST.get("customerName")
        CarID =request.POST.get("CarID")
        CarModel =request.POST.get("CarModel")
        exist = Order.objects.filter(Order_ID = orderID)
        if (len(exist) == 0):
            insertNewOrder = Order()
            insertNewOrder.Order_ID = orderID
            insertNewOrder.Order_CreateDate = orderCreateDate
            insertNewOrder.Order_PickupDate = orderPickupDate
            insertNewOrder.Order_PickupStore = orderPickupStore
            insertNewOrder.Order_ReturnDate = orderReturnDate
            insertNewOrder.Order_ReturnStore = orderReturnStore
            insertNewOrder.Customer_ID = customerID
            insertNewOrder.Customer_Name = customerName
            insertNewOrder.Car_ID = CarID
            insertNewOrder.Car_Model = CarModel
            insertNewOrder.save()
        else:
            error_msg = "Order ID existed"
    
    orderCount = []
    orderCount = Order.objects.all().count()
    orderCount = [orderCount]
    order = Order.objects.all().order_by('Order_ID')
    return render(request,'carRental/orderoverview.html', {'error_msg':error_msg,'order': order,'orderCount': orderCount,'staffInfor': staffInfor})

bodyType = Order.objects.all().values_list('Car_BodyType', flat=True).distinct().order_by('Car_BodyType');
makeName = Order.objects.all().values_list('Car_MakeName', flat=True).distinct().order_by('Car_MakeName');
storeCity = someStoreMonthly.objects.all().values_list('Store_City', flat=True).distinct().order_by('Store_City');	


def freebrowsing(request):
		cname=[]
		if 'storeCity' in request.GET:
			cname = request.GET.get('storeCity')
		storeName = someStoreMonthly.objects.all().filter(Store_City = cname).values_list('Store_Name', flat = True).order_by('Store_Name').distinct()
		
		result=[]
		defaultsdate = timezone.now().strftime("%Y-%m-%d").split("-")
		defaultrdate = int(defaultsdate[2])+3
		days=[]
		days30=[]
		
		month31=[1,3,5,7,8,10,12]
		for j in range(31):
			 days.append(j+1)
		for j in range(30):
			 days30.append(j+1)
		if int(defaultsdate[1]) in month31:
			days=days
		else:
			days=days30
			
		bodyGroup = request.POST.getlist('bodytype')
		makeGroup = request.POST.getlist('make')
		
		if len(bodyGroup) == 0:
			bodyGroup = Order.objects.all().values_list('Car_BodyType', flat=True).distinct().order_by('Car_MakeName')
			if len(makeGroup) == 0:
				makeGroup = Order.objects.all().values_list('Car_MakeName', flat=True).distinct().order_by('Car_MakeName')
			if len(makeGroup) != 0:
				if makeGroup[0] == 'allmake':
					makeGroup = Order.objects.all().values_list('Car_MakeName', flat=True).distinct().order_by('Car_MakeName')
			for i in range(len(makeGroup)):
				makeResult = bodyGroup.filter(Car_MakeName = makeGroup[i]).values_list('Car_MakeName', "Car_BodyType", "Car_Series", "Car_SeatingCapacity").distinct().order_by('Car_MakeName')
				for j in range(len(makeResult)):
					result.append(makeResult[j])
					
		elif len(makeGroup) == 0:
			makeGroup = Order.objects.all().values_list('Car_MakeName', flat=True).distinct().order_by('Car_MakeName')
			if len(bodyGroup) != 0:
				if bodyGroup[0] == 'alltype':
					bodyGroup = Order.objects.all().values_list('Car_BodyType', flat=True).distinct().order_by('Car_MakeName')
					for i in range(len(makeGroup)):
						makeResult = bodyGroup.filter(Car_MakeName = makeGroup[i]).values_list('Car_MakeName', "Car_BodyType", "Car_Series", "Car_SeatingCapacity").distinct().order_by('Car_MakeName')
						for j in range(len(makeResult)):
							result.append(makeResult[j])
				else:
					for i in range(len(bodyGroup)):
						bodyResult = makeGroup.filter(Car_BodyType = bodyGroup[i]).values_list('Car_MakeName', "Car_BodyType", "Car_Series", "Car_SeatingCapacity").distinct().order_by('Car_MakeName')
						for j in range(len(bodyResult)):
							result.append(bodyResult[j])
			
		elif bodyGroup[0] == 'alltype':
			bodyGroup = Order.objects.all().values_list('Car_BodyType', flat=True).distinct().order_by('Car_MakeName')
			if len(makeGroup) != 0:
				if makeGroup[0] == 'allmake':
					makeGroup = bodyGroup.values_list('Car_MakeName', flat=True).distinct().order_by('Car_MakeName')
				for i in range(len(makeGroup)):
					makeResult = bodyGroup.filter(Car_MakeName = makeGroup[i]).values_list('Car_MakeName', "Car_BodyType", "Car_Series", "Car_SeatingCapacity").distinct().order_by('Car_MakeName')
					for j in range(len(makeResult)):
						result.append(makeResult[j])
		
		elif makeGroup[0] == 'allmake':
			makeGroup = Order.objects.all().values_list('Car_MakeName', flat=True).distinct().order_by('Car_MakeName')
			if len(bodyGroup) !=0:
				for i in range(len(bodyGroup)):
					bodyResult = makeGroup.filter(Car_BodyType = bodyGroup[i]).values_list('Car_MakeName', "Car_BodyType", "Car_Series", "Car_SeatingCapacity").distinct().order_by('Car_MakeName')
					for j in range(len(bodyResult)):
						result.append(bodyResult[j])
						
		elif (len(bodyGroup) != 0):
			if (bodyGroup[0] != 'alltype'):
				if len(makeGroup) != 0:
					for i in range(len(bodyGroup)):
						bodyResult = Order.objects.filter(Car_BodyType = bodyGroup[i]).values_list('Car_MakeName', "Car_BodyType", "Car_Series","Car_SeatingCapacity").distinct()
						for k in range(len(makeGroup)):
							makeResult = bodyResult.filter(Car_MakeName = makeGroup[k]).values_list('Car_MakeName', "Car_BodyType", "Car_Series","Car_SeatingCapacity").distinct().order_by('Car_MakeName')
							for j in range(len(makeResult)):
								result.append(makeResult[j])
							
		resultCounter = len(result)
		if 'detail' in request.GET:
			detail = request.GET.getlist('informationtrans')
			if len(detail) == 0:
				return render(request, 'carRental/freebrowsing.html',{'bodyType': bodyType, 'makeName' : makeName, 'storeCity':storeCity, 'storeName':storeName,'result': result, 'resultCounter':resultCounter})
			make,series = detail[0].split("+")
			carbt = Order.objects.filter(Car_MakeName = make, Car_Series=series).values_list("Car_BodyType").distinct()
			carsc = Order.objects.filter(Car_MakeName = make, Car_Series=series).values_list("Car_SeatingCapacity").distinct()
			
			informationshow = Order.objects.filter(Car_MakeName = make, Car_Series=series).values_list("Car_Model","Car_SeriesYear","Car_PriceNew","Car_EngineSize"
			,"Car_FuelSystem","Car_TankCapacity","Car_Power","Car_StandardTransmission","Car_Drive","Car_Wheelbase","Car_ID").distinct();
			typeID = len(informationshow)
			cartrans = Order.objects.filter(Car_MakeName = make, Car_Series=series).values_list()
			cardv = Order.objects.filter(Car_MakeName = make, Car_Series=series).values_list()
			return render(request, 'carRental/detailpage.html',{'detail':detail, 'bodytype':carbt, 'seats':carsc,'make':make,'series':series, 'informationshow':informationshow, 'typeID':typeID})
		return render(request, 'carRental/freebrowsing.html',{'days':days,'defaultrdate':defaultrdate,'defaultsdate':defaultsdate,'bodyType': bodyType, 'makeName' : makeName, 'storeCity':storeCity, 'storeName':storeName,'result': result, 'resultCounter':resultCounter})
		

def storerecord(request):
    return render(request, 'carRental/storerecord.html',{'storeGroup': storeGroup})
	
def about(request):
	return render(request, 'login/about.html')

def staffinformation(request):
    error_username = ""
    if request.method == "POST":
        account = request.POST.get("staffAccount")
        check = User.objects.filter(username=account)
        if (len(check) == 0):
            error_username = "The username (" + account + ") doesn't exist"
        else:
            position = request.POST.get("staffPosition")
            User.objects.filter(username=account).update(first_name = position)
            StaffInformation.objects.filter(PhoneNumber=account).update(Position = position)
    staffInfor = StaffInformation.objects.all()
    return render(request, 'carRental/staffInformation.html',{ 'error_username':error_username ,'staffInfor': staffInfor,})

def recommend(request):
    #Amount of cars and ordered by amount
    orderedByCarList = []
    city = request.GET['city']
    month = request.GET['month']
    if 'year' in request.GET:
        year = request.GET.get("year")
        month = request.GET.get("month")
        if city != '':
            city = request.GET.get("city")
            monthoutcome = Order.objects.filter(Order_PickupDate__istartswith = year + month).filter(Pickup_Store_City = city)
            
        else:
            monthoutcome = Order.objects.filter(Order_PickupDate__istartswith = year + month)
        orderedByCar = monthoutcome.values_list("Car_BodyType").annotate(total_car = Count('Car_BodyType')).order_by('-total_car')
        year = [year]
        month = [month]
        city = [city]
        #total amount of order in this month
        totalCount = [monthoutcome.count()]
        for i in range(len(orderedByCar)):
            for j in range(len(orderedByCar[i])):
                orderedByCarList.append(orderedByCar[i][j])
        if month == '':
            return render(request, 'login/homepage.html')
        else:
            return render(request, 'login/homepage.html', {'orderedByCarList': orderedByCarList[0:1], 'numberofCar':orderedByCarList[1:2], 'year': year, 'month': month, 'totalCount': totalCount, 'city': city})
        
    return render(request, 'login/homepage.html')


def contactus(request):
    return render(request, 'carrental/contact.html')
