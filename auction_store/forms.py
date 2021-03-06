from django import forms
from .models import Bid, Item, Order
from users.models import Cart

END_DATE = ['24H', '4 Day', '10 Days']


class BidForm(forms.ModelForm):
  class Meta:
    model = Bid
    fields = ['amount']


class CreateForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ['image', 'name', 'category',
              'price', 'start_auction_price',
              'condition', 'origin_country', 'previous_owners',
              'short', 'desc', 'link_read_more']
    # widgets = {'start_date': forms.HiddenInput()}


class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ['full_name', 'phone_number', 'street_address1',
              'street_address2', 'town_or_city', 'country', 'postcode',
              'order_price', 'buyer', 'item_name', 'county']
    widgets = {
        'order_price': forms.HiddenInput(),
        'buyer': forms.HiddenInput(),
        'item_name': forms.HiddenInput(),
    }
