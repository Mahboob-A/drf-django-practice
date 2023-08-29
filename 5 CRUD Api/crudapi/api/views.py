from ast import parse
from urllib import request
from django.shortcuts import render

from io import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
# CRUD API Using DRF 

from .serializer import ArtistSerializer, AlbumSerializer, SongSerializer
from .models import Artist, Album, Song


@method_decorator(csrf_exempt, name='dispatch')
class ArtistAPI(View): 
        def get(self, request, *args, **kwargs): 
                json_data = request.body 
                stream = BytesIO(json_data)
                parser_data = JSONParser().parse(stream)
                id = parser_data.get('id', None)
                
                if id is not None: 
                        try: 
                                single_artist_data = Artist.objects.get(id=id)
                                serializer = ArtistSerializer(single_artist_data)
                                json_data = JSONRenderer().render(serializer.data)
                                return HttpResponse(json_data, content_type='application/json')
                                                        
                        except ObjectDoesNotExist: 
                                response_data = {'msg' : f'The id {id} is not valid.'}
                                json_data = JSONRenderer().render(response_data)
                                return HttpResponse(json_data, content_type='application/json')
                        
                # if id is not provided, then pass all the data 
                all_artist_data = Artist.objects.all()
                serializer = ArtistSerializer(all_artist_data, many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
        
        def post(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                artist_name = parsed_data.get('artist_name', None)

                # if any required field is not provided, then the below serializer.errors will provide the errors 
                serializer = ArtistSerializer(data=parsed_data)
                if serializer.is_valid(): 
                        serializer.save()
                        response_data = {'msg' : f'Artist data with name - {artist_name} is successfully created !!'}
                        json_data = JSONRenderer().render(response_data)
                        return HttpResponse(json_data, content_type='application/json')
        
                # if anything goes wrong, return the errors 
                json_data = JSONRenderer().render(serializer.errors)
                return HttpResponse(json_data, content_type='application/json')
        
        
        def put(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                id = parsed_data.get('id', None)
                
                if isinstance(id, int): 
                        try : 
                                single_artist_data = Artist.objects.get(id=id)
                                old_artist_name = single_artist_data.artist_name
                                serializer = ArtistSerializer(single_artist_data, data=parsed_data, partial=True) # partial update 
                                if serializer.is_valid(): 
                                        serializer.save()
                                        response_data = {
                                                'msg' : f'Artists data with name - {old_artist_name} is successfully updated !!',
                                        }
                                        json_data = JSONRenderer().render(response_data)
                                        return HttpResponse(json_data, content_type='application/json')

                                # handle cases where any errors happens 
                                json_data = JSONRenderer().render(serializer.errors)
                                return HttpResponse(json_data, content_type='application/json')
                                
                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'This id - {id} is invalid !!',
                                }
                                json_data = JSONRenderer().render(response_data)
                                return HttpResponse(json_data, content_type='application/json')
                        
                else: 
                        response_data = {
                                'msg' : 'Id is required to update data. !! If you are passing an Id, pass it as int type'
                        }
                        json_data = JSONRenderer().render(response_data)
                        return HttpResponse(json_data, content_type='application/json')   
                                
        def delete(self, request, *args, **kwargs): 
                json_data = request.body 
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                id = parsed_data.get('id', None)
                
                try: 
                        artist = Artist.objects.get(id=id)
                        artist_name = artist.artist_name 
                        artist.delete()
                        response_data = {
                                'msg' : f"The Artist with name - {artist_name} along with all of the Artist's accociated Album and Songs are is successfully deleted !!"
                        }
                        json_data = JSONRenderer().render(response_data)
                        return HttpResponse(json_data, content_type='application/json')
                except ObjectDoesNotExist: 
                        response_data = {
                                'msg' : f'The Artist ID - {id} is invalid !!'
                        }
                        return JsonResponse(response_data, safe=False)
                
                
@method_decorator(csrf_exempt, name='dispatch')
class AlbumAPI(View):
        
        def get(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                id = parsed_data.get('id', None)
               
                if id is not None: 
                       try : 
                                single_album_data = Album.objects.get(id=id)
                                serializer = AlbumSerializer(single_album_data)
                                json_data = JSONRenderer().render(serializer.data)
                                return HttpResponse(json_data, content_type='application/json')
                        
                       except ObjectDoesNotExist :
                               response_data = {
                                       'msg' : f'The Album ID - {id} is invalid or the Album might be deleted !!'
                               }
                               json_data = JSONRenderer().render(response_data)
                               return HttpResponse(json_data, content_type='application/json')
                
                # if id is None, then pass all the data 
                all_album_data = Album.objects.all()
                serializer = AlbumSerializer(all_album_data, many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
        
        
        def post(self, request, *args, **kwargs): 
                json_data = request.body 
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                artist_id = parsed_data.get('artist', None)
                
                if artist_id is not None: 
                        try : 
                                artist = Artist.objects.get(id=artist_id)
                                artist_name = artist.artist_name 
                                album_name = parsed_data.get('album_name', None)
                                serializer = AlbumSerializer(data=parsed_data)
                                if serializer.is_valid(): 
                                        serializer.save()
                                        response_data = {'msg' : f'Album with the name - {album_name} of the Artist - {artist_name} is successfully created !!'}
                                        json_data = JSONRenderer().render(response_data)
                                        return HttpResponse(json_data, content_type='application/json')
                                
                                # return if any errors occures 
                                return JsonResponse(serializer.errors, safe=False)
                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The Artist ID - {artist_id} is invalid or it might be deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                
                response_data = {'msg' : 'Artist ID must be provided to create an Album !!'}
                json_data = JSONRenderer().render(response_data)
                return HttpResponse(json_data, content_type='application/json')
        
        def put(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                id = parsed_data.get('id', None)
      
                if isinstance(id, int): 
                        try : 
                                single_album_data = Album.objects.get(id=id)
                                old_album_name = single_album_data.album_name
                                serializer = AlbumSerializer(single_album_data, data=parsed_data, partial=True)
                                if serializer.is_valid(): 
                                        serializer.save()
                                        response_data = {
                                                'msg' : f'The album - {old_album_name} is successfully updated !!'
                                        }
                                        json_data = JSONRenderer().render(serializer.data)
                                        return HttpResponse(json_data, content_type='application/json')
                                
                                # return if there are any errors 
                                json_data = JSONRenderer().render(serializer.errors)
                                return HttpResponse(json_data, content_type='application/json')

                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The album id - {id} is invalid !! '
                                }
                                return JsonResponse(response_data, safe=False)
                
                # if id is not passed as int or id is not passed, then respose. passing id as str will also work, but if 
                # forget to pass the id and pass any other string that is not int, then an error will occured. 
                response_data = {
                        'msg' : f'Did you forget to pass Album ID? Pass the Album ID as integer only'
                }
                return JsonResponse(response_data, safe=False)
        
        def delete(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                album_id = parsed_data.get('album_id', None)

                if album_id is not None: 
                        try : 
                                album_data = Album.objects.get(id=album_id)
                                album_name = album_data.album_name
                                artist_name = album_data.artist.artist_name
                                album_data.delete()
                                response_data = {
                                        'msg' : f'The Album - {album_name} of Artist - {artist_name}  is successfully deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The Album ID - {album_id} is invalid or it might be deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                
                # if artist id is not provided 
                response_data = {
                        'msg' : 'Album ID is required to delete an Album. Remember deleting an Album will result in deleting all the related Album Songs.'
                }
                return JsonResponse(response_data, safe=False)
                
        


@method_decorator(csrf_exempt, name='dispatch')
class SongAPI(View): 
        
        def get(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                id = parsed_data.get('id', None)
               
                if id is not None: 
                       try : 
                                single_song_data = Song.objects.get(id=id)
                                serializer = SongSerializer(single_song_data)
                                json_data = JSONRenderer().render(serializer.data)
                                return HttpResponse(json_data, content_type='application/json')
                        
                       except ObjectDoesNotExist :
                               response_data = {
                                       'msg' : f'The Song ID - {id} is invalid or the Song might be deleted!!'
                               }
                               json_data = JSONRenderer().render(response_data)
                               return HttpResponse(json_data, content_type='application/json')
                
                # if id is None, then pass all the data 
                all_song_data = Song.objects.all()
                serializer = SongSerializer(all_song_data, many=True)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
        
        
        def post(self, request, *args, **kwargs): 
                json_data = request.body 
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                album_id = parsed_data.get('album', None)
                song_name = parsed_data.get('song_name', None)
                
                if album_id is not None: 
                        try: 
                                album = Album.objects.get(id=album_id)
                                album_name = album.album_name
                                artist_name = album.artist.artist_name 
                                serializer = SongSerializer(data=parsed_data)
                                if serializer.is_valid(): 
                                        serializer.save()
                                        response_data = {
                                                'msg' : f'The Song - {song_name} is successfully created to the Album - {album_name} of the Artist - {artist_name} !!' 
                                        }
                                        json_data = JSONRenderer().render(response_data)
                                        return HttpResponse(json_data, content_type='application/json')
                                
                                # return if any error occures 
                                return JsonResponse(serializer.errors, safe=False)
                        
                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The Album ID - {album_id} is invalid or the Album might be deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                
                # if album id is not provided, album id is needed to add a song to a album 
                response_data = {
                        'msg' : 'Album ID must be provided to add a song to Album !!'
                }
                return JsonResponse(response_data, safe=False)
                        
                
        def put(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                id = parsed_data.get('id', None)
      
                if isinstance(id, int): 
                        try : 
                                single_song_data = Song.objects.get(id=id)
                                album_name = single_song_data.album.album_name
                                artist_name = single_song_data.album.artist.artist_name
                                
                                new_song_name = parsed_data.get('song_name', None)
                                old_song_name = single_song_data.song_name
                                
                                serializer = SongSerializer(single_song_data, data=parsed_data, partial=True)
                                if serializer.is_valid(): 
                                        serializer.save()
                                        response_data = {
                                                'msg' : f'The Song - {old_song_name} from Album - {album_name} of The Artist - {artist_name}  is successfully updated to - {new_song_name} !!'
                                        }
                                        json_data = JSONRenderer().render(response_data)
                                        return HttpResponse(json_data, content_type='application/json')
                                
                                # return if there are any errors 
                                json_data = JSONRenderer().render(serializer.errors)
                                return HttpResponse(json_data, content_type='application/json')

                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The Song ID - {id} is invalid or the Song might be deleted !! '
                                }
                                return JsonResponse(response_data, safe=False)
                
                # if id is not passed as int or id is not passed, then respose. passing id as str will also work, but if 
                # forget to pass the id and pass any other string that is not int, then an error will occured. 
                response_data = {
                        'msg' : f'Did you forget to pass Song ID? Pass the Song ID as integer only'
                }
                return JsonResponse(response_data, safe=False)
                                

        def delete(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                song_id = parsed_data.get('id', None)

                if song_id is not None: 
                        try : 
                                song = Song.objects.get(id=song_id)
                                song_name = song.song_name
                                album_name = song.album.album_name 
                                artist_name = song.album.artist.artist_name 
                                
                                song.delete()
                                
                                response_data = {
                                        'msg' : f'The Song - {song_name} from Album - {album_name} of the Artist - {artist_name}  is successfully deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                        
                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The Song ID - {song_id} is invalid or it might be deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                
                # if song id is not provided 
                response_data = {
                        'msg' : 'Song ID is required to delete a Song.'
                }
                return JsonResponse(response_data, safe=False)