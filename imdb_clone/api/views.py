from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import generics, mixins
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from imdb_clone.models import * 
from .serializers import *
from .permissions import *
from imdb_clone.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from imdb_clone.api.pagination import WatchListPagination,WatchListOSPagination,WatchListCPagination


# filtering current user reviews

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username) #using __ cause its froeginkey

    # query parameters

    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)

# generic api views (imp)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    throttle_classes = [ReviewCreateThrottle,AnonRateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    # this function using for to set new functin inside the generic api
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)  #finding the movie id (watchlist id)
        
        # one user can submit only one review for one movie
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user = review_user) #cheking if the user have submitted any review!
        
        # we are passing a if condition for if the user already submitted a review for that movie then we have to show a validation error
        if review_queryset.exists():
            raise ValidationError('You already submitted a review')
        
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
            
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
                
        serializer.save(watchlist=watchlist, review_user=review_user)
    
# class ReviewList(generics.ListCreateAPIView):
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated] its means only authenticated user can only read that list else we cant see that 
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']


    # instead of return all the objects we can filter according to the movie(watchlist)
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
        
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    



# generic views (mixins)
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request,*args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# for filter&search test 
class WatchListLV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination
    # permission_classes = [IsAuthenticated] its means only authenticated user can only read that list else we cant see that 
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    
    # filter test
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # search test
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title','=platform__name'] #using this = you have to enter correct sppeling 

    # ordering field test
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']

class WatchListAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    
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
            return Response(serializer.errors, status=400)
        

class WatchDetailAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
             return Response({'Error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #StreamPlatform 
class StreamPlatformAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        paltform = StreamPlatform.objects.all()
        serialzer = StreamPlatformSerializer(paltform, many=True)
        return Response(serialzer.data)
    
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
       
class StreamPlatformDetailAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    

    
    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
        