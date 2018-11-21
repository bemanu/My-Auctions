# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import json
from django.db.models import Count, Q
from django.shortcuts import  render
from .models import  AuctionViewed
from auctions.models import Auction


def auction_chart_view(request):
    dataset = Auction.objects.values('category').annotate(ON_GOING_count=Count('category', filter=Q(status='on going')), \
              ENDED_count=Count('category', filter=Q(status='ended'),\
                          NOT_AUCTIONED_count=Count('category', filter=Q(status='not auctioned'))))

    context = {
        'dataset': dataset
    }

    return render(request, 'analytics/category_chart.html', context)
