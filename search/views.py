from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from auctions.models import Auction, CATEGORY

from django.db.models import Q

class SearchAuctionView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchAuctionView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Auction.objects.search(query)
        return Auction.objects.all()


@login_required
def advanced_search(request):
    if request.method == 'POST':
        results = Auction.objects.filter().all()
        title = request.POST['title']
        category = request.POST['select']
        min = request.POST['min']
        max = request.POST['max']
        expiry_time = request.POST['Expiry time']

       
        print (title)
        print (category)
        print (min)
        print (max)
        print (expiry_time)



        if title:
            print ('first if : ', title)
            results = results.filter(title__icontains=title)
            for it in results:
                print(it.title)
        elif expiry_time:
            print( 'in expirey time ')
            results = Auction.objects.deadline_filter(results,expiry_time)
            print(expiry_time)
        elif category:
            print('in category')
            results = results.filter(category__icontains=category)
            print(category)

        elif min :
            print ('in price min')
            results = results.filter(min_price__gte=min)
            print(min)
        elif max:
            print('in prce max')
            results = results.filter(min_price__lte=max)
            print(max)
        elif min and max :
            print('i price min and max')
            results = results.filter(min_price__gte=min,min_price__lte=max)
            print('min %d   max %d', min,max)
        # else:
        #     results = Auction.objects.search('')

        context = {
            'results': results
        }
        return render(request, "search/advanced_search_view.html", context)
    else:
        cat = []
        for q in CATEGORY:
            cat.append(q[1])
        context = {
            'CATEGORY': cat
        }
        return render(request, 'search/advanced_search.html', context)
