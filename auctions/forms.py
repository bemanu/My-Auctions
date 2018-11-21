from .models import Auction
from django.forms import ModelForm
from django import forms


class AuctionOfferForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            "min_price",
            'offer',
            "high_bidder",
        ]


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            'category',

            'title',
            'image',
            'description',
            "min_price",

        ]


class EditForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            'title',
            'image',
            'description',
        ]


class SearchForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            'category',
        ]

# class WallForm(ModelForm):
#     class Meta:
#         model = Auction
#         fields = [
#
#         ]
