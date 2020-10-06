from listing.models import Listing, SpecialPrice
from tests.conftest import SpecialPriceFactory, UserFactory, ListingFactory, listing
from account.models import User

import pytest


pytestmark = pytest.mark.django_db #

class TestUser:
    
    def test_create_user(self, user):
        email = user.email # we instantiate user
        assert User.objects.all().count() == 1
        assert User.objects.last().email == email

    def test_user__str__(self, user):
        assert user.__str__() == user.email

    def test_incomplete_user(self):
        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(TypeError):
            User.objects.create_user(email='')
        with pytest.raises(TypeError):
            User.objects.create_user(email='', password="foo")

    def test_incomplete_superuser(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='super@user.com',
                password='foo',
                name='John',
                is_superuser=False
            )

class TestListing:

    def test_create_listing(self):
        user = UserFactory.create()
        
        ListingFactory(owner=user, name='asd')
        
        assert Listing.objects.all().count() == 1
        assert Listing.objects.last().name == 'asd'


class TestSpecialPrice:

    def test_create_special_price(self, listing):
        # listing_containing_prices = listing
        assert SpecialPrice.objects.all().count() == 3