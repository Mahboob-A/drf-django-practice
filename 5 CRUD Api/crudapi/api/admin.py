from django.contrib import admin

# Register your models here.
from .models import Artist, Album, Song

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin): 
        list_display = ['id', 'artist_name', 'genre']
        
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin): 
        list_display = ['id', 'album_name', 'artist', 'total_songs', 'first_publication', 'last_updated']
        
@admin.register(Song)
class SongAdmin(admin.ModelAdmin): 
        list_display = ['id', 'song_name', 'album', 'song_name', 'first_publication', 'last_updated']
        

