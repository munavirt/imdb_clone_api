from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.WatchListAv.as_view(),name='movie_list'),
    path('<int:pk>/',views.WatchDetailAv.as_view(),name='movie_details'),
    
    path('new-list/',views.WatchListLV.as_view(),name="movie-det"),#testign filter

    path('stream/', views.StreamPlatformAv.as_view(),name='stream_list'),
    path('stream/<int:pk>/',views.StreamPlatformDetailAv.as_view(),name='stream_detail'),
    
    path('<int:pk>/review-create/',views.ReviewCreate.as_view(),name='review-create'),
    # int:pk = movie id (watchlist id)
    path('<int:pk>/review/',views.ReviewList.as_view(),name='review-list'), #its going like stream/id number of watchlist/then all the reviews of that id number
    path('review/<int:pk>/',views.ReviewDetail.as_view(),name='review_detail'),
    path('reviews/<str:username>/',views.UserReview.as_view(),name='user-review'),

    path('reviews/',views.UserReview.as_view(),name='user-reviews')
]