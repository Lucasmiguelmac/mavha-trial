from django.contrib import admin
from django.urls.conf import include, path

app_name = 'mavha_trial'

urlpatterns = [
    path('secure_admin/', admin.site.urls),
    path('api/', include('listing.api.urls')),
]
