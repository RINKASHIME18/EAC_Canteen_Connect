from django.urls import path
from .views import (
    home, login_view, register_view, logout_view, 
    report_concern, report_history, rate_view, suggestion_view
)

urlpatterns = [
    path('', home, name='home'),
    path('report/', report_concern, name='report_concern'),
    path('rate/', rate_view, name='rate_view'),
    path('suggest/', suggestion_view, name='suggestion_view'),
    path('history/', report_history, name='report_history'),
    path('orders/', report_history, name='report_history'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]