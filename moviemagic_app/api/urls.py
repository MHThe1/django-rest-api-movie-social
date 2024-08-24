from django.urls import path, include
# from moviemagic_app.api.views import movie_list, movie_details
from moviemagic_app.api.views import MovieList, MovieDetails

urlpatterns = [
    path('list/', MovieList.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetails.as_view(), name='movie-details'),

]
