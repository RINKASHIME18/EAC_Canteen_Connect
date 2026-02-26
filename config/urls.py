from django.contrib import admin
from django.urls import path, include # Add 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('canteen.urls')), # Connects the app to the main site
]