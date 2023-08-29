from django.db import models
from django.urls import reverse 
# Create your models here.

#  Artist, Album, Song 

class Artist(models.Model): 
        artist_name = models.CharField(max_length=30)
        genre = models.CharField(max_length=15)
        
        def __str__(self): 
                return self.artist_name
        

class Album(models.Model): 
        artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
        album_name = models.CharField(max_length=30)
        total_songs = models.IntegerField()
        first_publication = models.DateField(auto_now_add=True)
        last_updated = models.DateField(auto_now=True)
        
        def __str__(self): 
                return self.album_name
        

class Song(models.Model): 
        album = models.ForeignKey(Album, on_delete=models.CASCADE)
        song_name = models.CharField(max_length=50)
        first_publication = models.DateField(auto_now_add=True)
        last_updated = models.DateField(auto_now=True)
        
        def __str__(self): 
                return self.song_name
        
        def get_absolute_url(self):
                return reverse("model_detail", kwargs={"pk": self.pk})
        
                
