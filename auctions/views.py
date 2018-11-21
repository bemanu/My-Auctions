from datetime import date, time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404 , JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import DetailView, ListView

from accounts.models import Profile
from analytics.signals import object_viewed_signal
from auctions.models import *
from .forms import *
from .models import Auction
from .models import CATEGORY


class AuctionListView(ListView):
    template_name = "auctions/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Auction.objects.all()


def auction_list_view(request):
    queryset = Auction.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'auctions/list.html', context)


def delete_auction(request, auction_id):
    Auction.objects.filter(id=auction_id).delete()
    return HttpResponseRedirect('/accounts/profile/')


# class AuctionDetailSlugView(UpdateView):
#     queryset = Auction.objects.all()
#     template_name = "auctions/detail.html"
#
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get('slug')
#
#         try:
#             instance = Auction.objects.get(slug=slug, active=True)
#         except Auction.DoesNotExist:
#             raise Http404("Not found.")
#         except Auction.MultipleObjectsReturned:
#             qs = Auction.objects.filter(slug=slug, active=True)
#             instance = qs.first()
#         except:
#             raise Http404("Nothing found")
#         return instance
#


class AuctionDetailView(DetailView):
    template_name = "auctions/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AuctionDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        # context['abc'] = 123
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Auction.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Auction doesn't exist")
        object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance

    def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Auction.objects.filter(pk=pk)


def auction_detail_view(request, auction_id):
    print("Im in the view ")
    instance = Auction.objects.get(pk=auction_id)
    # outbid = Auction.objects.minimum_bid(instance.offer)

    if request.method == 'POST':
        # outbid = float(Auction.objects.minimum_bid(instance.offer))
        profile = Profile.objects.get(user=request.user)
        curr_offer = float(request.POST['Offer'])

        if curr_offer >= instance.offer:
            instance = bid(instance, request.POST['Offer'], profile)
            instance.save()

        else:
            messages.error(request, "Invalid offer.")
        path = ('/auctions/detail/' + str(auction_id))
        return HttpResponseRedirect(path)
    else:
        time_left = (instance.deadline - timezone.now()).total_seconds()
        minimum_offer = instance.min_price
        # if instance.offer > 0:
        #     minimum_offer = float(instance.offer) + float(outbid)
        context = {
            'instance': instance,
            'remain_time': time_left,
            # 'bid': outbid,
            'minimum_offer': minimum_offer
        }
        return render(request, 'auctions/detail.html', context)


@login_required
def create_auction(request):
    if request.method == 'POST':
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            new_auction = Auction()
            new_auction.title = request.POST['title']
            new_auction.image = form.cleaned_data['image']
            new_auction.description = request.POST['description']
            new_auction.vendor = request.user
            new_auction.min_price = request.POST['min_price']
            new_auction.deadline = request.POST['dataScadenza']
            new_auction.auction_type = request.POST['auction_type']
            # end_date = request.POST['dataScadenza']
            # print("======================AUCTION======================")
            # print("title :", new_auction.title)
            # print("description :", new_auction.description)
            # print("deadline :", new_auction.deadline)
            # # print("inserted date  :", end_date)
            # print("vendor :", new_auction.vendor)
            # print("base price  :", new_auction.min_price)
            # print("===============END==================================")
            try:
                print('in try state')
                end_date = request.POST['dataScadenza']
                print(end_date)
                a, m, g = str(end_date).split('-')
                a = int(a)
                m = int(m)
                g = int(g)
                expiry_date = date(a, m, g)
                # print(type(expiry_date))
                # print('expiry date  : ', end_date)
                # print('today: ', date.today())
                # print(expiry_date < date.today())
                # today_date = datetime.datetime.now().date()
                # print('todays date ', today_date)
                print('about to do the if control')
                if expiry_date < date.today():
                    messages.error(request, 'Invalid date inserted')
                    #         print("======================AUCTION======================")
                    #         print("title :", new_auction.title)
                    #         print("description :", new_auction.description)
                    #         print("deadline :", new_auction.deadline)
                    #         print("deadline :", end_date)
                    #         print("vendor :", new_auction.vendor)
                    #         print("base price  :", new_auction.min_price)
                    #         print("===============END==================================")
                    return HttpResponseRedirect('.')
            except:
                print("In the excption")
                messages.error(request, 'Incorrect form')
                return HttpResponseRedirect('/auctions/create_auction/')

            else:
                expiry_time = request.POST['oraScadenza']
                h, m = str(expiry_time).split(':')
                h = int(h) - 2
                m = int(m)
                expiry_time = time(h, m)
                # print(type(end_time))
                closes_at = datetime.combine(expiry_date, expiry_time)
                # datetime(end_date, end_time)
                new_auction.deadline = closes_at
                new_auction.category = request.POST['category']
                new_auction.active = True
                new_auction.save()
                return HttpResponseRedirect('/auctions/')

        else:
            print("Invalid form")
            return HttpResponseRedirect('/auctions/create_auction/')
    else:
        form = AuctionForm()
        category = []
        for q in CATEGORY:
            category.append(q[0])
            context = {
                'form': form,
                'CATEGORY': category
            }
            return render(request, 'auctions/new_auction.html', context)


@login_required
def upcoming_auctions_view(request):
    # form = SearchForm()
    Auction.objects.update_deadline()
    lst = Auction.objects.divid_by_cate()
    list = Auction.objects.deadline_filter(Auction.objects.all(), TIME_LIMIT)
    print(type(list))
    print(len(list))
    context = {
        'obj_list': list,
        'cate':lst,

    }
    return render(request, 'auctions/wall.html', context)


def mine_auction(request):
    obj = Auction.objects.filter(vendor__username=request.user.username)
    context = {
        'object_list': obj

    }
    return render(request, 'auctions/m_auctions.html', context)


def partecipated_auction(request):
    user = Profile.objects.get(user=request.user)
    obj = Auction.objects.filter(id__in=user.mine_auctions.all().filter(active=False))
    print(len(obj))
    for item in obj:
        print(item.title)
    context = {

        'object_list': obj
    }
    return render(request, 'auctions/partecipated_auctions.html', context)


def get_data(request):
    return render(request,'auctions/graph_view.html', {})


def get_view_data(request):
    print('ciao')
    qs = []
    # categories = []
    categories = ['comics','computer parts','collections','others', ]
    for obj in categories:
        items_active  = Auction.objects.filter(active=False, category__exact=obj).count()
        items_nactive = Auction.objects.all().filter(category__exact=obj).count()
        qs.append(items_nactive)
        qs.append(items_active)

    labels = [
        'Active comics','Nactive comics','Active computer parts','Nactive Computer Parts','Active collections',
        'Nactive collection', 'Active others', 'Nactive others',
    ]
    default_items = qs
    data = {
        'labels': labels,
        'default': default_items

        }
    print(default_items)
    print(data)
    # print(categories)
    return JsonResponse(data)
