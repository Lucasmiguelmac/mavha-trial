from account.models import User
from listing.models import Listing, SpecialPrice
from rest_framework import serializers
from hashid_field.rest import HashidSerializerCharField

class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model
    """
    
    id              = HashidSerializerCharField(source_field='listing.Listing.id')
    owner_id        = serializers.PrimaryKeyRelatedField(
        pk_field=HashidSerializerCharField(source_field='account.User.id'),
        read_only=True,
    )
    special_prices  = serializers.StringRelatedField(many=True)

    class Meta:
        model   = Listing
        fields  =   ['id', 'name', 'slug',
                    'description', 'adults', 'children',
                    'pets_allowed', 'base_price', 'cleaning_fee',
                    'image_url', 'weekly_discount', 'monthly_discount',
                    'special_prices', 'owner_id']


class ListingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Listings
    """
    owner   = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model   = Listing
        exclude = ['id', 'slug']


class ListingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Listings
    """

    class Meta:
        model   = Listing
        fields  =   ['name', 'description', 'adults',
                    'children', 'pets_allowed', 'base_price',
                    'cleaning_fee', 'image_url', 'weekly_discount',
                    'monthly_discount']



class SpecialPriceSerializer(serializers.ModelSerializer):    
    """
    Serializer to create special price
    """
    date = serializers.DateField()

    class Meta:
        model   = SpecialPrice
        fields  = ['date', 'price']