from django.urls import path, include
from rest_framework.routers import DefaultRouter

from moviemagic_app.api.views import (WatchListAV, WatchListGV, WatchListDetailsAV, StreamPlatformVS, 
                                      ReviewList, ReviewDetail, ReviewCreate, UserReviewList)


router = DefaultRouter()
router.register(r'platform', StreamPlatformVS, basename='platform')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('alt-list/', WatchListGV.as_view(), name='watch-list-alt'),
    
    path('<int:pk>/', WatchListDetailsAV.as_view(), name='watch-details'),
    
    path('', include(router.urls)),
    
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='reviews-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/', UserReviewList.as_view(), name='user-review-detail'),
    

]
