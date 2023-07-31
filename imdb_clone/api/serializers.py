from rest_framework import serializers
from imdb_clone.models import *


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchlist',)

class WatchListSerializer(serializers.ModelSerializer):

    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    class Meta:
        model = WatchList
        fields = "__all__"
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    # nested serialization
    watch_list = WatchListSerializer(many=True, read_only=True)
    
    # string related field
    # watch_list = serializers.StringRelatedField(many=True)
    # it will be show you returned str in models.py
    
    # hyperlink related Field
    # tracks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-detail')
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"