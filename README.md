# Mavha Trial

_This is a trial project for a position as a Django dev for Mavha._

## Set up

1) Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `requirements.txt`. You might want to install this inside a virtual environment.
    ```bash
    pip install requirements.txt
    ```
2) This API was made using PostgreSQL. In order to setup a db you'll have to first create a db in postgres:
    ```bash
    sudo su postgres
    psql
    create database your_database_name;
    \q
    exit
    ```
    and right after modify your Django database settings in `settings.py` properly:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'TEST': {
                'NAME': 'test_db',
            },
        }
    }
    ```
## Usage
After seeting up the project you can locally run the project in your terminal sitting in the root folder (the directory that contains `manage.py`) and running the following:

```bash
python manage.py runserver
```

## Documentation

| Method | Endpoint | Detail |
| ------ | ------ | ------ |
| GET | /api/listings/ | Show all listings | 
| POST | /api/listings/ | Create a listing |  
| GET | /api/listings/<hash_id>/ | Retrieve a listing |  
| PUT | /api/listings/<hash_id>/ | Modify a listing |  
| DELETE | /api/listings/<hash_id>/ | Delete a listing |
| POST | /api/listings/<hash_id>/special-prices/ | Create a special price |
| DELETE | /api/listings/<hash_id>/special-prices/<sp_id>/ | Delete a special price |
| POST | /api/listings/<hash_id>/checkout/ | Calculate cost |

### Show all listings

>GET: /api/listings/

>200 OK
```
[
    {
        "id": "xJLgnXN",
        "name": "Lake House (ex Artist Work Develop Series.)",
        "slug": "lake-house-ex-artist-work-develop-series-xjlgnxn",
        "description": "House in the NahuelHuapi lake",
        "adults": 1,
        "children": 1,
        "pets_allowed": false,
        "base_price": "0.00",
        "cleaning_fee": null,
        "image_url": null,
        "weekly_discount": null,
        "monthly_discount": null,
        "special_prices": [],
        "owner_id": "aDP7DXy"
    },
    {
        "id": "9QXqopJ",
        "name": "Lake House",
        "slug": "lake-house-9qxqopj",
        "description": "House in the NahuelHuapi lake",
        "adults": 1,
        "children": 1,
        "pets_allowed": false,
        "base_price": "0.00",
        "cleaning_fee": null,
        "image_url": null,
        "weekly_discount": null,
        "monthly_discount": null,
        "special_prices": [
            "9.47 - 2020-10-02",
            "9.47 - 2020-10-02",
            "9.47 - 2020-10-02"
        ],
        "owner_id": "vELmzpO"
    }
]
```

## Testing
In order to run tests, in your terminal sitting in the root folder (the directory that contains `manage.py`) and running the following:

```bash
pytest
```