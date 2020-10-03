from listing.models import Listing, SpecialPrice
from tests.conftest import SpecialPriceFactory, UserFactory, ListingFactory
from account.models import User

import pytest

class TestUser:
    
    @pytest.mark.django_db
    def test_create_user(self):
        UserFactory(email='someone@gmail.com')

        assert User.objects.all().count() == 1
        assert User.objects.last().email == 'someone@gmail.com'

    @pytest.mark.django_db
    def test_incomplete_user(self):
        with pytest.raises(TypeError):
            User.objects.create_user()
        with pytest.raises(TypeError):
            User.objects.create_user(email='')
        with pytest.raises(TypeError):
            User.objects.create_user(email='', password="foo")

    @pytest.mark.django_db
    def test_incomplete_superuser(self):
        with pytest.raises(ValueError):
            User.objects.create_superuser(
                email='super@user.com',
                password='foo',
                name='John',
                is_superuser=False
            )

class TestListing:

    @pytest.mark.django_db
    def test_create_listing(self):
        user = UserFactory.create()
        
        ListingFactory(owner=user, name='asd')
        
        assert Listing.objects.all().count() == 1
        assert Listing.objects.last().name == 'asd'


class TestSpecialPrice:

    @pytest.mark.django_db
    def test_create_special_price(self):
        user = UserFactory.create()
        listing = ListingFactory.create(owner=user)

        SpecialPriceFactory.create(listing=listing, price=23.00)

        assert SpecialPrice.objects.all().count() == 1
        assert SpecialPrice.objects.last().price == 23.00