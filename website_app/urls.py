from website import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from website_app import views
from .views import review, about

urlpatterns = [
    path('home/',views.home),
    path('menu',views.menu),
    # path('about',views.about),
    path('review/', review, name='review'),
    path('about/', about, name='about'),
    path('contact',views.contact),
    path('place_order',views.Ordertable),
    path('register',views.user_register,name='register'),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    # path('catfilter1/<cv>',views.catfilter1),
    path('sort/<sv>',views.sort),
    path('sort/<av>',views.sorta),
    path('range',views.range),
    path('cdetails/<cid>',views.coffee_details),
    path('gallery',views.gallery),
    path('addtocart/<cid>',views.addtocart),
    path('viewcart',views.viewcart),
    path('index',views.index),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

