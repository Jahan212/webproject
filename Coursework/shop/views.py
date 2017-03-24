from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Profile, Product, Basket
from django.contrib.auth import (authenticate, get_user_model, login, logout,)
from .forms import UserLoginForm, UserSignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json as simplejson

# Create your views here.

@login_required(login_url='login/')
def index(request):
    #return the homepage
    products = Product.objects.all()
    return render(request, "shop/home.html", {"products":products})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = UserLoginForm(request.POST or None)

    title = "Login"
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")

    return render(request, "shop/login.html", {"form":form, "title": title})


@login_required(login_url='login/')
def logout_view(request):
    logout(request)
    return redirect('/login/')


def register_view(request):
    form = UserSignUpForm(request.POST or None)

    title = "Register"
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        address_line = form.cleaned_data.get('address_line')
        post_code = form.cleaned_data.get('post_code')
        phone_number = form.cleaned_data.get('phone_number')
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')

        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        user.profile.address_line = address_line
        user.profile.post_code = post_code
        user.profile.phone_number = phone_number
        user.save()
        return redirect("login")
    return render(request, "shop/login.html", {"form":form, "title": title})


@login_required(login_url='login/')
def basket_view(request):
    basket = Basket.objects.filter(user=request.user)
    total = 0
    for item_info in basket:
        total += item_info.product.price * item_info.quantity

    return render(request, "shop/basket.html", {"baskets":basket, "total":total})


@login_required(login_url='login/')
def checkout(request):
    user = request.user
    items = Basket.objects.filter(user = user)
    total = 0
    receipt = "Your receipt is: \n"

    for item in items:
        sub_total = item.product.price * item.quantity
        receipt += "Product name: " + item.product.name + ", Quantity: " + str(item.quantity) + ", sub total: " + str(sub_total) + "\n"
        total += sub_total
        item.delete()

    receipt += "Final total : " + str(total)
    #email receipt to user
    user.email_user("Checkout confirmation: Thanks for your purchase!", receipt)

    messages.success(request, "Your order is complete. We have sent you a confirmation email")

    return redirect("/")


@login_required(login_url='login/')
def add_item(request):
    response_dict= {
        'success': True,
    }
    item_id = request.GET.get('id')
    user = request.user;
    product = get_object_or_404(Product, pk = item_id)
    basket_entry, created = Basket.objects.get_or_create(
        user = user,
        product = product
    )
    if not created:
        basket_entry.quantity += 1;
    basket_entry.save()

    print("complete")
    response_dict = {
        'product_id':item_id
    }
    return HttpResponse(simplejson.dumps(response_dict), content_type='application/json')


@login_required(login_url='login/')
def search(request):
    #orderby = request.GET.get("orderby")
    query = request.POST.get("search-term")
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = None

    context = dict(results=results, query=query)
    return render(request, 'shop/results.html', context)


@login_required(login_url='login/')
def remove_item(request):

    item_id = request.GET.get('id')
    product = get_object_or_404(Product, pk=item_id)
    instance = Basket.objects.get(user=request.user, product=product)
    instance.delete()


    response = "complete"
    return HttpResponse(response, content_type='text')


@login_required(login_url='login/')
def minus_item(request):

    item_id = request.GET.get('id')
    product = get_object_or_404(Product, pk=item_id)
    instance = Basket.objects.get(user=request.user, product=product)
    print(instance)
    if(instance.quantity == 1):
        instance.delete()
    else:
        print(instance.quantity)
        instance.quantity -= 1
        instance.save()

    response = "complete"
    return HttpResponse(response, content_type='text')
