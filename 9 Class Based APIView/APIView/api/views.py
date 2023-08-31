from functools import partial
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

from .models import Student
from .serializer import StudentSerializer


class StudentAPI(APIView): 
        
        def get(self, request, id=None, format=None): 
                if id: 
                        try : 
                                student = Student.objects.get(id=id)
                                serializer = StudentSerializer(student)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                        except ObjectDoesNotExist: 
                                return Response({'msg' : 'The ID Does Not Exist !!'}, status=status.HTTP_400_BAD_REQUEST)
                        
                students = Student.objects.all()
                serializer = StudentSerializer(students, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        def post(self, request, format=None): 
                try: 
                        data = request.data 
                        serializer = StudentSerializer(data=data)
                        if serializer.is_valid(): 
                                serializer.save()
                                return Response({'msg' : 'Student Created Successfully !!', 'data' : serializer.data}, status=status.HTTP_201_CREATED)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Exception: 
                        return Response({'msg' : 'Something Bad Happened !!'}, status=status.HTTP_400_BAD_REQUEST)
                
        def put(self, request, id=None, format=None): 
                if id: 
                        try: 
                                data = request.data 
                                student = Student.objects.get(id=id)
                                serializer = StudentSerializer(student, data=data)
                                if serializer.is_valid(): 
                                        serializer.save()
                                        return Response({'msg' : 'Complete Data Update Is Successfull !!'}, status=status.HTTP_200_OK)
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        except ObjectDoesNotExist: 
                                return Response({'msg' : 'The ID Does Not Exist !!'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg' : 'ID Must Be Provided To Update Complete Data !!'}, status=status.HTTP_400_BAD_REQUEST)
        
        def patch(self, request, id=None, format=None): 
                if id: 
                        try: 
                                data = request.data 
                                student = Student.objects.get(id=id)
                                serializer = StudentSerializer(student, data=data, partial=True)
                                if serializer.is_valid(): 
                                        serializer.save()
                                        return Response({'msg' : 'Partial Data Update Is Successfull !!'}, status=status.HTTP_200_OK)
                                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        except ObjectDoesNotExist: 
                                return Response({'msg' : 'The ID Does Not Exist !!'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg' : 'ID Must Be Provided To Update Partial Data !!'}, status=status.HTTP_400_BAD_REQUEST)
                
        def delete(self, request, id=None, format=None): 
                if id: 
                        try : 
                                student = Student.objects.get(id=id)
                                name = student.name
                                student.delete()
                                return Response({"msg" : f"{name}'s Data Is Deleted Successfully !!"}, status=status.HTTP_200_OK)
                        except ObjectDoesNotExist: 
                                return Response({'msg' : 'The ID Does Not Exist !!'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'msg' : 'ID Must Be Provided To Delete Data !!'}, status=status.HTTP_400_BAD_REQUEST)
                                


