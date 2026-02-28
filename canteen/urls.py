from django.urls import path
from .views import (
    home, login_view, register_view, logout_view, 
    report_concern, report_history, rate_view, suggestion_view, activity_feed, mark_activity_read,
    admin_concerns, admin_ratings, admin_suggestions
)

urlpatterns = [
    path('', home, name='home'),
    path('report/', report_concern, name='report_concern'),
    path('rate/', rate_view, name='rate_view'),
    path('suggest/', suggestion_view, name='suggestion_view'),
    path('history/', report_history, name='report_history'),
    path('activity/', activity_feed, name='activity_feed'),
    path('monitor/concerns/', admin_concerns, name='admin_concerns'),
    path('monitor/ratings/', admin_ratings, name='admin_ratings'),
    path('monitor/suggestions/', admin_suggestions, name='admin_suggestions'),
    path('activity/read/<str:activity_type>/<int:activity_id>/', mark_activity_read, name='mark_activity_read'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]