from django.urls import path
from moviemagic_app.api.views import (WatchListAV, WatchListDetailsAV, 
                                      StreamPlatformListAV, StreamPlatformDetailsAV, 
                                      ReviewList, ReviewDetail)

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='watch-details'),
    path('platformlist/', StreamPlatformListAV.as_view(), name='streaming-list'),
    path('platform/<int:pk>', StreamPlatformDetailsAV.as_view(), name='platform-details'),
    path('review', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),

]
