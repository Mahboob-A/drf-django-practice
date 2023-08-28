
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
# artist.get_data()
# artist.post_data()
# artist.update_data(1, 'Mahboob Alam', 'EVM Drops')

# artist.delete_data(14)


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
                
        def delete_data(self, artist_id):
                data = {'artist' : artist_id}
                json_data = json.dumps(data)
                resp = requests.delete(url=self.URL, data=json_data)
                print(resp)
                print(resp.json())
                


album = AlbumApiData(14, 'Kul Album', 20)
# album.post_data()
# album.get_data()
# album.update_data(3, 2, 'Roar - New Life', 7)
album.delete_data(14)


                