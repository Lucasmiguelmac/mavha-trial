from decimal import Decimal
from itertools import chain
from listing.models import Listing, SpecialPrice
from account.models import User
from factory.fuzzy import FuzzyText
from factory.django import DjangoModelFactory

from datetime import datetime, timedelta
import factory
import random
import pytest

#======================================FACTORIES=======================================
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    name        = factory.Faker('name')
    email       = factory.Faker('email')
    password    = factory.Faker('password')


class ListingFactory(DjangoModelFactory):
    class Meta:
        model = Listing
    owner               = factory.SubFactory(UserFactory)
    name                = factory.Faker('sentence', nb_words=4)
    description         = factory.Faker('sentence', nb_words=10)
    base_price          = float(Decimal(random.randrange(5000,20000))/100)
    adults              = factory.Faker('random_number')
    children            = factory.Faker('random_number')
    pets_allowed        = random.choices([True, False])[0]
    cleaning_fee        = float(Decimal(random.randrange(100, 5000))/100)
    image_url           = factory.Faker('image_url')
    weekly_discount     = float(Decimal(random.randrange(100, 5000))/100)
    monthly_discount    = float(Decimal(random.randrange(100, 5000))/100)

class SpecialPriceFactory(DjangoModelFactory):
    class Meta:
        model = SpecialPrice
    listing = factory.SubFactory(ListingFactory)
    date    = factory.Faker('date_object')
    price   = float(Decimal(random.randrange(500, 1000))/100)
#=======================================FIXTURES=======================================
@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def listing():
    listing = ListingFactory(owner=UserFactory())
    SpecialPriceFactory.create_batch(3, listing=listing)
    return listing
#========================================UTILS=========================================
def to_dict(instance):
    """
    Turns model into a dict
    https://stackoverflow.com/a/29088221/12010568
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


def random_date_between(start_date, end_date, date_format='%Y-%m-%d'):
    start_date_datetime = datetime.strptime(start_date, date_format)
    time_delta = datetime.strptime(end_date, date_format) - start_date_datetime
    days_from_start = random.randrange(0, abs(time_delta.days)) 
    
    random_date = start_date_datetime + timedelta(days=days_from_start)
    random_date = random_date.strftime(date_format)

    return random_date