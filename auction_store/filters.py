import django_filters
from .models import *
from django.db.models import Q


class ItemFilter(django_filters.FilterSet):

    price_g = django_filters.NumberFilter(label='€ Price',
                                          field_name='price', lookup_expr='gt')
    price_l = django_filters.NumberFilter(label='Range',
                                          field_name='price', lookup_expr='lt')
    multi_name_fields = django_filters.CharFilter(label='',
                                                  method='filter_by_all_name_fields')

    FORMAT_CHOICES = (
        ('all', 'All Listings'),
        ('auction', 'Auction'),
        ('end_auction', 'Ended Auction'),
        ('sale', 'Only Sale'),
        ('sold', 'Sold')
    )

    format = django_filters.ChoiceFilter(
        label="Format", choices=FORMAT_CHOICES, method='filter_by_format')

    SORT_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
        ('low_price', 'Low Price'),
        ('high_price', 'High Price'),
    )

    sort = django_filters.ChoiceFilter(
        label="Sort", choices=SORT_CHOICES, method='filter_by_sort')

    SELLER_CHOICES = (
        ('store', 'Store'),
        ('private', 'Private'),
    )

    seller = django_filters.ChoiceFilter(
        label="Seller", choices=SELLER_CHOICES, method='filter_by_seller')

    class Meta:
        model = Item
        fields = ['category', 'price', 'name', 'desc',
                  'price', 'seller', 'buyer', 'category', 'winner']

    def filter_by_sort(self, queryset, name, value):
        if value == 'newest':
            x = '-start_date'
        elif value == 'oldest':
            x = 'start_date'
        elif value == 'high_price':
            x = '-price'
        elif value == 'low_price':
            x = 'price'
        return queryset.order_by(x)

    def filter_by_format(self, queryset, name, value):
        if value == 'auction':
            queryset = queryset.filter(
                end_date__gte=timezone.now(), in_auction=True, sold=False)
        elif value == 'end_auction':
            queryset = queryset.filter(
                end_date__lt=timezone.now(), sold=False, in_auction=True)
        elif value == 'sale':
            queryset = queryset.filter(
                Q(sold=False, winner__isnull=True, end_date__lt=timezone.now()) | Q(sold=False, in_auction=False))
        elif value == 'sold':
            queryset = queryset.filter(sold=True)
        else:
            queryset = queryset.all()
        return queryset

    def filter_by_seller(self, queryset, name, value):
        if value == 'store':
            queryset = queryset.filter(seller__is_superuser=True)
        elif value == 'private':
            queryset = queryset.exclude(seller__is_superuser=True)
        return queryset.order_by('seller')

    def filter_by_all_name_fields(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(category__icontains=value) | Q(desc__icontains=value) | Q(price__icontains=value) | Q(seller__username=value) | Q(buyer__username=value) | Q(winner__username=value))
