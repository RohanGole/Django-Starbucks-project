from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from website_app.models import items,Cart,Order,ordertable
from django.db.models import Q
from random import randrange
from .models import CustomerReview
import razorpay
from datetime import datetime

# Create your views here.
def home(request):
    context={}
    c=items.objects.filter(is_active=True).order_by('?')[:6]
    context['items']=c
    print(c)
    return render(request,'home.html',context)
 

def menu(request):
    context={}
    c=items.objects.filter(is_active=True)
    context['items']=c
    print(c)
    return render(request,'menu.html',context)

def about(request):
    reviews = CustomerReview.objects.order_by('-id')[:3]
    return render(request, 'about.html', {'reviews': reviews})

def contact(request):
    return render(request,'contact.html')

def Ordertable(request):
    if request.method == 'POST':
        pname = request.POST['name']
        phoneno = request.POST['phone']
        email = request.POST['email']
        noofcoffee = request.POST['people']
        address = request.POST['message']
        print(pname,phoneno,email,noofcoffee,address)
        context={}
        if pname=="" or phoneno=="" or noofcoffee=="" or address=="" :
            context['prrmsg']="fields cannot be empty.."
            return render(request,'place_order.html',context)
        else:
            u=ordertable.objects.create(name=pname,phoneno=phoneno,noofcoffee=noofcoffee,address=address,email=email)           
            # u=authenticate(name=pname,phoneno=phoneno,noofcoffee=noofcoffee,address=address,email=email)           
            u.save()
            return render(request,'place_order.html',context)
    else:
     return render(request,'place_order.html') # slide def is temperory        
    



def user_register(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="feilds cannot be empty.."
            return render(request,'register.html',context)
        elif upass != ucpass:
            context['errmsg']="password and confirm password didn't match.."
            return render(request,'register.html',context)
        else:  
            try:  
                u = User.objects.create(username=uname, password=upass,email=uname)
                u.set_password(upass)       #encrypt format
                u.save()
                context['success']="User created successfully"
                return render(request, 'register.html',context)
            except Exception:
                context['errmsg']="user with same username already present.."
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')

    

def user_login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="fields cannot be empty.."
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            if u is not None:
                login(request,u)    # start the session
                return redirect('home/')
            else:
                context['errmsg']="Invalid username and password.."
                return render(request,'login.html',context)            
    else:
     return render(request,'login.html')
 
def user_logout(request):
    logout(request)
    return redirect('home/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    c=items.objects.filter(q1 & q2)
    context={}
    context['items']=c
    return render(request,"menu.html",context)

# def catfilter(request,cv):
#     q1=Q(is_active=True)
#     q2=Q(cat=cv)
#     c=items.objects.filter(q1 & q2)
#     context={}
#     context['items']=c
#     return render(request,"home.html",context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    c=items.objects.filter(q1 & q2 & q3)
    context={}
    context['items']=c
    return render(request,"menu.html",context)

def sort(request,sv):
    if sv=='0':
        col="price"  #ascending order
    else:
        col="-price"   # descending order 
    c=items.objects.filter(is_active=True).order_by(col)
    context={}
    context['items']=c
    return render(request,"menu.html",context)


def sorta(request,av):
    if av=='0':
        col="price"  #ascending order
    else:
        col="-price"   # descending order 
    c=items.objects.filter(is_active=True).order_by(col)
    context={}
    context['items']=c
    return render(request,"menu.html",context)

def coffee_details(request,cid):
    c=items.objects.filter(id=cid)
    context={}
    context['items']=c
    return render(request,"coffee_details.html",context)

def gallery(request):
    return render(request,'gallery.html')

def addtocart(request,cid):
    if request.user.is_authenticated:
        userid=request.user.id 
        u=User.objects.filter(id=userid)
        print(u[0])   # user object
        c=items.objects.filter(id=cid)
        print(c[0])    # items object
        q1=Q(uid=u[0])
        q2=Q(cid=c[0])
        c1=Cart.objects.filter(q1 & q2)
        n=len(c1)
        context={}
        context['items']=c
        if n==1:
            context['msg']="Product added successfully !!"
        else:
            c1=Cart.objects.create(uid=u[0],cid=c[0])
            c1.save()
            context['success']="Product added successfully !!"
        return render(request,"coffee_details.html",context)
    else:
        return redirect("/login")
    


def index(request):
    return render(request,'index.html') #timpass

def viewcart(request):
    c1=Cart.objects.filter(uid=request.user.id)
    s=0
    nc=len(c1)
    for x in c1:
        s=s+x.cid.price * x.qty 
    print(s)
    context={}
    context["coffee"]=c1
    context['total']=s
    context['n']=nc
    return render(request,"cart.html",context)


def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c)             #object queryset
    print(c[0])          #object
    print(c[0].qty)      #quantity only
    if qv == '1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:      #1>1=F
            t=c[0].qty-1
            c.update(qty=t)    
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    print(userid)
    c=Cart.objects.filter(uid=userid)
    print(c)
    oid=randrange(1000,9999)
    print("order_id: ",oid)
    for x in c:
        o=Order.objects.create(Order_id=oid,uid=x.uid,cid=x.cid,qty=x.qty)
        # o=Order.objects.create(Order_id=oid,uid=x.uid,pid=x.cid,qty=x.qty)
        o.save()
        x.delete()     # to delete previus cart data
        orders=Order.objects.filter(uid=request.user.id)
        context={}
        context['items']=orders
        np=len(orders)
        s=0
        for x in orders:
            s=s+x.cid.price*x.qty
        context['total']=s
        context['n']=np    
    return render(request,'placeorder.html',context)


def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.cid.price * x.qty
        oid=x.Order_id
    client = razorpay.Client(auth=("rzp_test_lbfRW5iyvcv9Xb", "5fyaso3SxSryHe9X2GU0xjZo"))
    data = { "amount": s*100, "currency": "MYR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)



# views.py
def review(request):
    if request.method == 'POST':
        customer_name = request.POST['customer_name']
        rating = request.POST['rating']
        review_text = request.POST['review_text']

        CustomerReview.objects.create(
            customer_name=customer_name,
            rating=rating,
            review_text=review_text
        )
        return redirect('about')

    return render(request, 'review.html')

def shop_location(request):
    return render(request, 'shop_location.html')

def catfilter(request,cv):
    if cv == "1":
        z="Our Special"
    elif cv == "2":
        z="Creamy"
    elif cv == "3":
        z="Chocolate"
    else:
        z="Cold Coffee"
    print(z)

    q1=Q(is_active=True)
    q2=Q(cat=cv)
    c=items.objects.filter(q1 & q2)
    context={}
    context['items']=c
    context['cat']=z
    return render(request,"menu.html",context)
