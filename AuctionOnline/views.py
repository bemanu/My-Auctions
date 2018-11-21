from __future__ import print_function
from __future__ import print_function

from django.db.models import Q
from django.shortcuts import render
from auctions.models import Auction


def home_page(request):
    upcomping_lst = Auction.objects.deadline_filter(Auction.objects.all(),3)
    print(len(upcomping_lst))
    if upcomping_lst:
        print('ok')
    else:
        print('none')

    item = Auction.objects.all()
    print('The number of objects actived',len(item))

    obj_list = Auction.objects.all().filter(~Q(id__in=upcomping_lst))

    print(len(obj_list))


    context = {
        'object_list': obj_list,
    }
    return render(request, 'home_page.html', context)

