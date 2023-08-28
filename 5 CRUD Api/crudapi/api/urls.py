
from django.urls import path 

from .views import ArtistAPI, AlbumAPI

urlpatterns = [
        path('artist/', ArtistAPI.as_view(), name='artist_api'),
        path('album/', AlbumAPI.as_view(), name='album_api'),
]
