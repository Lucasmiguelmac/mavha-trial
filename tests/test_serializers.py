import pytest
from rest_framework import serializers
from listing.api.serializers import ListingSerializer, ListingCreateSerializer, SpecialPriceSerializer
from tests.conftest import SpecialPriceFactory, UserFactory, ListingFactory, to_dict


class TestListingSerializers:
    
    @pytest.mark.django_db
    def test_listing_create_serializer_serialization(self):
        listings = ListingFactory.create_batch(3)
        serializer = ListingSerializer(listings, many=True)
        assert len(serializer.data) == 3

    @pytest.mark.django_db
    def test_listing_serializer_serialization(self):
        user = UserFactory()
        json_data = to_dict(ListingFactory.build(owner=user))
        # Add owner in serializer's format
        json_data['owner'] = user.id.hashid
        #Remove extra fields made by factory
        json_data.pop('id')
        json_data.pop('slug')
        serializer = ListingCreateSerializer(data=json_data)
        assert serializer.is_valid()
        data = serializer.validated_data
        assert set(data.keys()) == set(json_data.keys())

class TestSpecialPriceSerializers:
    
    @pytest.mark.django_db
    def test_serialization(self):
        listing = ListingFactory()
        json_data = to_dict(SpecialPriceFactory.build(listing=listing))
        json_data['listing'] = listing.id.hashid
        formated_date = str(json_data['date'])
        json_data['date'] = formated_date
        json_data.pop('id')
        json_data.pop('listing')
        serializer = SpecialPriceSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)
            
        assert serializer.is_valid()
        data = serializer.validated_data
        assert set(data.keys()) == set(json_data.keys())