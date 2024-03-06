from django.shortcuts import render, redirect
from .models import Mebel
from .forms import UpdateItemForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def create_paginator(request, mebels):
    paginator = Paginator(mebels, 30)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def show_all(request):
    mebels = Mebel.objects.all().order_by("-price")
    return render(
        request,
        'app_1/show_all.html',
        {'page_obj': create_paginator(request, mebels),
         'mebels': mebels}
    )


def show_all_admin(request):
    form = UpdateItemForm()
    mebels = Mebel.objects.all().order_by("-parse_datetime")
    return render(
        request,
        'app_1/show_admin_item.html',
        {'page_obj': create_paginator(request, mebels),
            'form': form,
            'mebels': mebels
        }
    )


def show_item(request, item_id):
    item = Mebel.objects.get(pk=item_id)
    return render(
        request,
        'app_1/show_item.html',
        {'item': item}
    )


def update_item(request, item_id):
    if request.method == 'POST':
        new_description = dict(request.POST).get('description', '')
        new_price = dict(request.POST).get('price', '')
        Mebel.objects.filter(pk=item_id).update(
            price=new_price[0],
            description=new_description[0]
        )
    return redirect('items_admin')


def delete_item(request, item_id):
    Mebel.objects.filter(pk=item_id).delete()
    return redirect('items_admin')


def main(request):
    return redirect('main')


def page_not_found(request, exception):
    return redirect('main')


def login(request):
    return render(request, 'app_1/register.html')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'
