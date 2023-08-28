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
                                'msg' : f'The Artist with name - {artist_name} is successfully deleted !!'
                        }
                        json_data = JSONRenderer().render(response_data)
                        return HttpResponse(json_data, content_type='application/json')
                except ObjectDoesNotExist: 
                        response_data = {
                                'msg' : f'The id {id} is invalid !!'
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
                                       'msg' : f'The id - {id} is invalid !!'
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
                        album_name = parsed_data.get('album_name', None)
                        serializer = AlbumSerializer(data=parsed_data)
                        if serializer.is_valid(): 
                                serializer.save()
                                responser_data = {'msg' : f'Album with the name - {album_name} is successfully created !!'}
                                json_data = JSONRenderer().render(responser_data)
                                return HttpResponse(json_data, content_type='application/json')
                
                responser_data = {
                                'msg' : 'Artist id must be provided to create an Album !!'
                        }
                json_data = JSONRenderer().render(responser_data)
                return HttpResponse(json_data, content_type='application/json')
        
        def put(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                id = parsed_data.get('id', None)
                print(id)
                if isinstance(id, int): 
                        try : 
                                single_album_data = Album.objects.get(id=id)
                                print(single_album_data)
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
                
                # if id id is not passed as int or id is not passed, then respose. passing id as str will also work, but if 
                # forget to pass the id and pass any other string that is not int, then an error will occured. 
                response_data = {
                        'msg' : f'Did you forget to pass Album ID? Pass the Album ID as integer only'
                }
                return JsonResponse(response_data, safe=False)
        
        def delete(self, request, *args, **kwargs): 
                json_data = request.body
                stream = BytesIO(json_data)
                parsed_data = JSONParser().parse(stream)
                
                artist_id = parsed_data.get('artist', None)
                
                if artist_id is not None: 
                        try : 
                                artist_data = Artist.objects.get(id=artist_id)
                                artist_name = artist_data.artist_name
                                artist_data.delete()
                                response_data = {
                                        'msg' : f'Artist with name - {artist_name} and all of the realted Album and Song data is successfully deleted !!'
                                }
                                return JsonResponse(response_data, safe=False)
                        except ObjectDoesNotExist: 
                                response_data = {
                                        'msg' : f'The Artist with ID {artist_id} is invalid !!'
                                }
                                return JsonResponse(response_data, safe=False)
                
                # if artist id is not provided 
                response_data = {
                        'msg' : 'Artist ID is required to delete Album or Song data'
                }
                return JsonResponse(response_data, safe=False)
                
        
                
                
                
                 
                                

