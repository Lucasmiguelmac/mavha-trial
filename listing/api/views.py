from datetime import datetime, timedelta
from os import stat
from types import new_class
from django.core.exceptions import ValidationError
from django.http import request
from django.utils.functional import new_method_proxy
from django.utils.text import slugify
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import api_view
from listing.api.serializers import ListingSerializer, ListingCreateSerializer, ListingUpdateSerializer, SpecialPriceSerializer
from listing.models import Listing, SpecialPrice
from rest_framework.response import Response



@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def listing_viewset(request, hash_id=None):
    try:

        #Retrieve
        if request.method == 'GET':

            # List
            if hash_id == None:
                listings = Listing.objects.all()
                serializer = ListingSerializer(listings, many=True) 
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Detail
            else:
                try:
                    listing = Listing.objects.get(id=hash_id)
                    serializer = ListingSerializer(listing)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Listing.DoesNotExist:
                    data = {
                        'message': 'Listing not found',
                    }
                    return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
        # Create
        elif request.method == 'POST':
            try:
                serializer = ListingCreateSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data = ListingSerializer(instance=Listing.objects.all().last()).data
                    return Response(data=data, status=status.HTTP_201_CREATED)                
            except Exception as e:
                data = {
                    'message': e,
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        # Delete
        elif request.method == 'DELETE':
            try:
                listing = Listing.objects.get(id=hash_id)
                deleted_listing_id = listing.id.hashid
                listing.delete()
                data = {
                    'id': deleted_listing_id
                }
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)
            except Listing.DoesNotExist:
                data = {
                    'message': 'Listing not found',
                }
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        # Update
        elif request.method == 'PUT':
            try:
                listing = Listing.objects.get(id=hash_id)
            except Listing.DoesNotExist:
                data = {
                    'message': 'Listing not found',
                }
                return Response(data=data, status=status.HTTP_404_NOT_FOUND)
            serializer = ListingUpdateSerializer(data=request.data)

            if serializer.is_valid():
                serialized_data = serializer.validated_data
                # We check for name changes and modify the slug accordingly
                listing.name                = serialized_data['name']
                listing.slug                = slugify(f'{listing.name}-{listing.id}')
                listing.description         = serialized_data['description']
                listing.adults              = serialized_data['adults']
                listing.children            = serialized_data['children']
                listing.pets_allowed        = serialized_data['pets_allowed']
                listing.base_price          = serialized_data['base_price']
                listing.cleaning_fee        = serialized_data['cleaning_fee']
                listing.image_url           = serialized_data['image_url']
                listing.weekly_discount     = serialized_data['weekly_discount']
                listing.monthly_discount    = serialized_data['monthly_discount']
                
                data = ListingSerializer(instance=Listing.objects.all().last()).data
                return Response(data=data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {
                    'message': f'{serializer.error_messages}'
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    # Catch unexpected exceptions
    except Exception as e:
        data = {
            'message': 'Internal problem, please contact an Airbnb representative',
        }
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST', 'DELETE'])
def special_price_viewset(request, hash_id, price_id=None):
    if request.method == 'POST':
        try:
            serializer = SpecialPriceSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serialized_data = serializer.validated_data
                listing = Listing.objects.get(id=hash_id)
                sp = SpecialPrice.objects.create(
                    listing=listing,
                    date=serialized_data['date'],
                    price=serialized_data['price']
                )
                serializer = SpecialPriceSerializer(instance=sp)
                return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)

        except Listing.DoesNotExist:
            data = {
                'message': 'Listing not found',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        try:
            sp = SpecialPrice.objects.get(id=price_id)
            deleted_special_price_id = sp.id.hashid
            sp.delete()
            data = {
                'id': deleted_special_price_id
            }
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)

        except Listing.DoesNotExist:
            data = {
                'message': 'Listing not found',
            }
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def checkout_view(request, hash_id):
    try:
        listing = Listing.objects.get(id=hash_id)
        special_price_qs   = SpecialPrice.objects.all().filter(listing=hash_id)
        data    = request.data

        date_format = '%Y-%m-%d'
        checkin  = data['checkin']
        checkout = data['checkout']
        
        nights_cost = 0
        td = datetime.strptime(checkout, date_format) - datetime.strptime(checkin, date_format)
        nights = abs(td.days)
        
        current_date = datetime.strptime(checkin, date_format)
        for i in range(nights):
            try:
                sp = special_price_qs.get(date=current_date)
                nights_cost += sp.price
            except SpecialPrice.DoesNotExist:    
                nights_cost += listing.base_price
            current_date += timedelta(days=1)

        discount = listing.weekly_discount + listing.monthly_discount

        data = {
            'nights_count': nights,
            'nights_cost': nights_cost,
            'discount': discount,
            'cleaning_fee': listing.cleaning_fee,
            'total': float(nights_cost - discount + listing.cleaning_fee)
        }
        return Response(data=data, status=status.HTTP_200_OK)

    except Listing.DoesNotExist:
        data = {
            'message': 'Listing not found'
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        data = {
            'message': 'Internal problem, please contact an Airbnb representative',
        }
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)