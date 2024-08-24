from rest_framework import serializers
from moviemagic_app.models import WatchList, StreamPlatform

class WatchListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = WatchList
        fields = "__all__"
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = WatchListSerializer(many=True, read_only=True)
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='watch-details'
    )
    class Meta:
        model = StreamPlatform
        fields = "__all__"
    