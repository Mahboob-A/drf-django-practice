
from rest_framework import serializers

from django.utils import timezone

from .models import Artist, Album, Song 


class ArtistSerializer(serializers.Serializer): 
        artist_name = serializers.CharField(max_length=30)
        genre = serializers.CharField(max_length=15)
        
        def create(self, validated_data): 
                return Artist.objects.create(**validated_data)
        
        # I have implemented 3 types of defining the update method below. see each method. 
        def update(self, instance, validated_data): 
                instance.artist_name = validated_data.get('artist_name', instance.artist_name)
                instance.genre = validated_data.get('genre', instance.genre)
                
                instance.save()
                return instance 


class AlbumSerializer(serializers.Serializer): 
        # while dealing with foreignkey, use PrimaryKeyRelatedField and pass the all objects to which model it has foreign realtionship in the queryset param 
        artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all()) # set many=True for manytomany realtionships 
        album_name = serializers.CharField(max_length=30)
        total_songs = serializers.IntegerField()
        first_publication = serializers.DateField(read_only=True)
        last_updated = serializers.DateField(read_only=True)
        
        def create(self, validated_data): 
                validated_data['first_publication'] = timezone.now().date()
                validated_data['last_updated'] = timezone.now().date()
                return Album.objects.create(**validated_data)
        
        # to know more about the implementation, read the attached gpt conversation 
        def update(self, instance, validated_data): 
                validated_data['last_updated'] = timezone.now().date()
                for attr, value in validated_data.items(): 
                        if value is not None: 
                                setattr(instance, attr , value)

                # or can be used this 
                # instance.artist = validated_data.get('artist', instance.artist)
                # instance.album_name = validated_data.get('album_name', instance.album_name)
                # instance.total_songs = validated_data.get('total_songs', instance.total_songs)
                
                instance.save()
                return instance

class SongSerializer(serializers.Serializer): 
        # id = serializers.IntegerField()
        album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all()) 
        song_name = serializers.CharField(max_length=50)
        first_publication = serializers.DateField(read_only=True)
        last_updated = serializers.DateField(read_only=True)

        def create(self, validated_data): 
                validated_data['first_publication'] = timezone.now().date()
                validated_data['last_updated'] = timezone.now().date()
                return Song.objects.create(**validated_data)
        
        # to know more about the implementation, read the attached gpt conversation 
        def update(self, instance, validated_data): 
                validated_data['last_updated'] = timezone.now().date()
                for attr, value in validated_data.items(): 
                        if value is not None: 
                                setattr(instance, attr, value)
                        
                # instance.save(update_fields=validated_data.values()) # does not work 
                instance.save()
                return instance 