
import requests 
import json

class ArtistApiData: 
        URL = 'http://127.0.0.1:8000/api/artist/'
        
        def __init__(self, artist_name, genre): 
                self.artist_name = artist_name
                self.genre = genre 
                
        
        def get_data(self, id = None): 
                data = {}
                if id is not None: 
                        data = {'id' : id}
                json_data = json.dumps(data)
                resp = requests.get(url=self.URL, data=json_data)
                json_data = resp.json()
                print(resp)
                print(json_data)
        
        def post_data(self): 
                data = {
                        'artist_name' : self.artist_name, 
                        'genre' : self.genre, 
                }
                
                json_data = json.dumps(data)
                
                resp = requests.post(url=self.URL, data=json_data)
                json_data = resp.json()
                print(resp)
                print(json_data)
        
        def update_data(self, id = None, artist_name=None, genre=None): 
                data = {
                        'id' : id, 
                        'artist_name' : artist_name, 
                        'genre' : genre, 
                }
                json_data = json.dumps(data)
                resp = requests.put(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                
        def delete_data(self, id): 
                data = {'id' : id}
                json_data = json.dumps(data)
                resp = requests.delete(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                

artist = ArtistApiData('Demo user now', 'demo genre')
# artist.get_data()      # pass id to get specific data or pass empty to get all the artist data 
# artist.post_data()     # pass the artist name and the genre of the artist 
# artist.update_data(1, 'Mahboob Alam', 'EVM Drops')     # pass the artist id, new artist name and the new genre to update an aritst 

artist.delete_data(10)     # pass the artist id to delete artist. 


class AlbumApiData: 
        URL = 'http://127.0.0.1:8000/api/album/'
        
        def __init__(self, artist_id, album_name, total_songs): 
                self.artist_id = artist_id
                self.album_name = album_name
                self.total_songs = total_songs
                
        def get_data(self, id = None):
                data = {}
                if id is not None: 
                        data = {'id' : id}
                json_data = json.dumps(data)
                resp = requests.get(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                
                
        def post_data(self): 
                data = {
                        'artist' : self.artist_id, 
                        'album_name' : self.album_name, 
                        'total_songs' : self.total_songs
                }
                json_data = json.dumps(data)
                resp = requests.post(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                
        def update_data(self, artist_id,  album_id,   album_name=None, total_songs=None):
                data = {
                        'artist' : artist_id, 
                        'id' : album_id,
                        'album_name' : album_name, 
                        'total_songs' : total_songs,  
                }
                json_data = json.dumps(data)
                resp = requests.put(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                
        def delete_data(self, album_id):
                data = {'album_id' : album_id}
                json_data = json.dumps(data)
                resp = requests.delete(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                


album = AlbumApiData(10, ' Another demo Album', 25)  # artist id, album name, total songs 
# album.post_data()    # pass the artist id, album name, total songs to create an album 
# album.get_data(8)  # pass album id or pass no id to get all the album data 
# album.update_data(1, 1, 'Kara Sevda Songs', 14)  # artist id, album id, new album title, and total songs 
# album.delete_data(9) # album id to delete 



class SongApiData: 
        URL =  'http://127.0.0.1:8000/api/song/'
        
        def __init__(self, album_id, song_name): 
                self.album_id = album_id
                self.song_name = song_name
                
        def get_data(self, id = None):
                data = {}
                if id is not None: 
                        data = {'id' : id}
                json_data = json.dumps(data)
                resp = requests.get(url=self.URL, data=json_data)
                print(resp)
                print(resp.json()) 
                
                
        def post_data(self): 
                data = {
                        'album' : self.album_id, 
                        'song_name' : self.song_name, 
                }
                json_data = json.dumps(data)
                resp = requests.post(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                
        def update_data(self, song_id,  new_song_name):
                data = {
                        'id' : song_id, 
                        'song_name' : new_song_name, 
                }
                json_data = json.dumps(data)
                resp = requests.put(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                
        def delete_data(self, song_id):
                data = {'id' : song_id}
                json_data = json.dumps(data)
                resp = requests.delete(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())

song = SongApiData(12, 'Mar Java')   # pass the album id and the song name to add a song in that album 
# song.post_data()   # pass the album id and the song name to add a song in that album 
# song.get_data(23)    # pass id to get specific song data, else pass empty to get all songs data 

# song.update_data(23, 'Tum Ho Ho')  # pass the song id and the new name of the song to update the song name 

# song.delete_data(4)  # pass the song id to delete the song 