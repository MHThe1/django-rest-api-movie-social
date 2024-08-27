from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from moviemagic_app.api.permissions import IsAdminOrReadOnly, IsReviewerOrReadOnly
from moviemagic_app.models import WatchList, StreamPlatform, Review
from moviemagic_app.api.serializers import (WatchListSerializer, StreamPlatformSerializer, 
                                            ReviewSerializer)
from moviemagic_app.api.throttling import ReviewRateThrottle, ReviewListThrottle
from moviemagic_app.api.pagination import WatchListPagination, WatchListLimitOffsetPagination, WatchListCursorPagination

class UserReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    # def get_queryset(self):
    #     username = self.kwargs.get('username')
    #     return Review.objects.filter(reviewer_user__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(reviewer_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer  
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewRateThrottle]

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        
        reviewer_user = self.request.user
        reviewer_queryset = Review.objects.filter(watchlist=movie, reviewer_user=reviewer_user)
        
        if reviewer_queryset.exists():
            raise ValidationError("You have already reviewed this one!")
        
        if movie.number_of_ratings == 0:
            movie.average_rating = serializer.validated_data['rating']
        else:
            movie.average_rating = (movie.average_rating + (serializer.validated_data['rating'] * movie.number_of_ratings) ) / (movie.number_of_ratings + 1)
            
        movie.number_of_ratings += 1
        movie.save()
        
        serializer.save(watchlist=movie, reviewer_user=reviewer_user)

        
        

class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer_user__username', 'watchlist', 'active']
    
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewerOrReadOnly]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    
    
class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListLimitOffsetPagination

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=title', 'platform__name']

    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating']
    

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        
        return Response(serializer.data)
    
    def post(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

