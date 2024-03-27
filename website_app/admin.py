from django.contrib import admin
from website_app.models import items
from .models import CustomerReview


class itemsAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','is_active']
    list_filter=['cat','is_active']

# Register your models here.
admin.site.register(items,itemsAdmin) 



# admin.py
@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'created_at')
    search_fields = ('customer_name',)



