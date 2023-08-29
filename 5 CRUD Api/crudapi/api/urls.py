
from django.urls import path 

from .views import ArtistAPI, AlbumAPI, SongAPI

urlpatterns = [
        path('artist/', ArtistAPI.as_view(), name='artist_api'),
        path('album/', AlbumAPI.as_view(), name='album_api'),
        path('song/', SongAPI.as_view(), name='song_api'),
]
