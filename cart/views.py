from django.shortcuts import render,redirect,get_object_or_404
from shop.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def cart_details(request,tot=0,count=0,count_item=None):
    try:
        ct=cartlist.objects.get(cart_id=c_id(request))
        ct_items=items.objects.filter(cart=ct,active=True)
        for i in ct_items:
            tot +=(i.prodt.price*i.quan)
            count+=i.quan
    except ObjectDoesNotExist: 
        pass
    return render(request,'cart.html',{'ci':ct_items,'t':tot,'cn':count})
def c_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session_key.create()
    return ct_id
def add_cart(request,product_id):
    prod=products.objects.get(id=product_id)
    try:
        ct=cartlist.objects.get(cart_id=c_id(request))
    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request))
        ct.save()
    try:
        c_item=items.objects.get(prodt=prod,cart=ct)
        if c_item.quan<c_item.prodt.stock:
            c_item.quan+=1
            c_item.save()
    except items.DoesNotExist:
        c_item=items.objects.create(prodt=prod,quan=1,cart=ct)
        c_item.save()
    return redirect('cartDetails')
def min_cart(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prod=get_object_or_404(products,id=product_id)
    ct_items=items.objects.get(prodt=prod,cart=ct)
    if ct_items.quan>1:
        ct_items.quan-=1
        ct_items.save()
    else:
        ct_items.delete()
    return redirect('cartDetails')
def cart_delete(request,product_id):
    ct=cartlist.objects.get(cart_id=c_id(request))
    prod=get_object_or_404(products,id=product_id)
    ct_items=items.objects.get(prodt=prod,cart=ct)
    ct_items.delete()
    return redirect('cartDetails')

