from os import name
from django.urls.conf import path
from .views import listing_viewset, special_price_viewset, checkout_view


app_name = 'listing'

urlpatterns = [
    
    path('listings/',                                   listing_viewset,        name='listings'),
    path('listings/<hash_id>/checkout/',                checkout_view,          name='checkout'),
    path('listings/<hash_id>/special-prices/<sp_id>/',  special_price_viewset,  name='special-price'),
    path('listings/<hash_id>/special-prices/',          special_price_viewset,  name='special-prices'),
    path('listings/<hash_id>/',                         listing_viewset,        name='listing'),

]