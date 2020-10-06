from datetime import time, datetime
import random
from django.http import request
from django.http import response
from listing.models import Listing, SpecialPrice
from django_mock_queries.query import MockSet
from listing.api.serializers import ListingCreateSerializer, ListingSerializer, ListingUpdateSerializer, ListingSerializer
from .conftest import ListingFactory, SpecialPriceFactory, UserFactory, random_date_between, to_dict
from django.urls import reverse
from listing.api.views import checkout_view, listing_viewset, special_price_viewset
import json
import pytest

class TestListingViews:
    
    @pytest.mark.django_db
    def test_get_listings(self, rf):
        ListingFactory()
        url = reverse('listing:listings')
        request = rf.get(url)

        response = listing_viewset(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    @pytest.mark.django_db
    def test_retrieve_listing(self, rf):
        listing = ListingFactory()
        url = reverse('listing:listing', kwargs={'hash_id': listing.id.hashid})
        request = rf.get(url)

        response = listing_viewset(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    @pytest.mark.django_db
    def test_create_listing(self, rf):
        listing = ListingFactory()
        url = reverse('listing:listings')
        post_data = to_dict(listing)
        request = rf.post(url, post_data)

        response = listing_viewset(request).render()

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_update_listing(self, rf, listing):
        original_listing = listing
        original_owner = listing.owner
        updated_listing = ListingFactory.build(owner=original_owner)
        url = reverse('listing:listing', kwargs={'hash_id': listing.id.hashid})
        dict_data = to_dict(updated_listing)
        dict_data['id'] = original_listing.id.hashid
        dict_data['owner'] = original_owner.id.hashid
        post_data = json.dumps(dict_data)
        request = rf.put(url, post_data, content_type='application/json')

        response = listing_viewset(request, original_listing.id.hashid).render()

        assert response.status_code == 202

    @pytest.mark.django_db
    def test_retrieve_listing(self, rf, listing):
        hash_id = listing.id.hashid
        url = reverse('listing:listing', kwargs={'hash_id': hash_id})
        request = rf.delete(url)

        response = listing_viewset(request, hash_id).render()
        
        assert response.status_code == 204
        assert len(Listing.objects.all()) == 0

class TestSpecialPriceViews:
    
    @pytest.mark.django_db
    def test_delete_special_price(self, rf, listing):
        hash_id = listing.id.hashid
        special_prices = SpecialPrice.objects.all()
        special_price_count = special_prices.count()
        special_price = special_prices.last()
        sp_id = special_price.id.hashid
        url = reverse(
            'listing:special-price',
            kwargs={
                'hash_id': hash_id,
                'sp_id': sp_id,
            },
        )
        request = rf.delete(url)
        response = special_price_viewset(request, hash_id, sp_id).render()

        assert response.status_code == 204
        assert len(SpecialPrice.objects.all()) == special_price_count - 1

    @pytest.mark.django_db
    def test_calculate_special_price(self, rf, listing):
        #Setup
        checkin = '2020-10-28'
        checkout = '2020-11-5'
        date_format = '%Y-%m-%d'
        #Calculate expected total
        nights_td = datetime.strptime(checkout, date_format) - datetime.strptime(checkin, date_format)
        nights = abs(nights_td.days)
        sp = SpecialPriceFactory.create(
            listing=listing,
            date=random_date_between(checkin, checkout)
        )
        cleaning_fee = listing.cleaning_fee
        discounts = listing.weekly_discount + listing.monthly_discount
        nights_cost = sp.price + listing.base_price * (nights - 1)
        expected_total = nights_cost - discounts + cleaning_fee
        #Make request
        url = reverse(
            'listing:checkout',
            kwargs={
                'hash_id': listing.id.hashid,
            },
        )
        post_dict = {
            'checkin': checkin,
            'checkout': checkout,
        }
        request = rf.post(url, post_dict)
        response = checkout_view(request, listing.id.hashid).render()

        assert response.status_code == 200

        actual_total = response.data['total']

        assert round(expected_total, 2) == actual_total