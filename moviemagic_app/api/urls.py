from django.urls import path, include
from rest_framework.routers import DefaultRouter

from moviemagic_app.api.views import (WatchListAV, WatchListDetailsAV, StreamPlatformVS, 
                                      ReviewList, ReviewDetail, ReviewCreate)


router = DefaultRouter()
router.register(r'platform', StreamPlatformVS, basename='platform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name='watch-details'),
    
    path('', include(router.urls)),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),

]
