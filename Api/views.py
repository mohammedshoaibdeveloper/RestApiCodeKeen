from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from .models import *
from.serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token




##################################### Decorators ##################################### 

@api_view(['GET'])
def home(request):

    student_obj = Student.objects.all()
    serdata = StudentSerializer(student_obj,many=True).data
    return Response({'status':200,'data':serdata})


@api_view(['POST'])
def post_student(request):

    serializer = StudentSerializer(data = request.data)

    if not serializer.is_valid():
        return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

    serializer.save()
    return Response({'status':200,'data':serializer.data,'message':'your data is saved'})


@api_view(['PUT'])
def update_student(request,id):

    try:
        studentobj = Student.objects.get(id=id)

        serializer = StudentSerializer(studentobj,data = request.data)

        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

        serializer.save()
        return Response({'status':200,'data':serializer.data,'message':'your data is saved'})   

    except Exception as e:

        return Response({'status':403,'message':'invalid id'})


@api_view(['PATCH'])
def update_studentpartially(request,id):
    try:
        studentobj = Student.objects.get(id=id)
        

        serializer = StudentSerializer(studentobj,data = request.data, partial=True)

        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

        serializer.save()
        return Response({'status':200,'data':serializer.data,'message':'your data is saved'})   

    except Exception as e:
        print("e------------------------",e)
        return Response({'status':403,'message':'invalid id'})


@api_view(['DELETE'])
def delete_student(request,id):

    try:
        studentobj = Student.objects.get(id=id)
        studentobj.delete()
        return Response({'status':200,'message':'Deleted'}) 

    except Exception as e:
        print("e------------------------",e)
        return Response({'status':403,'message':'invalid id'})


@api_view(['GET'])
def get_book(request):
    book_obj  = Book.objects.all()
    serializer = BookSerializer(book_obj,many=True).data
    return Response({'status':200,'data':serializer})

##################################### Decorators ##################################### 


##################################### API view #####################################    

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

################# jwt authorization #################

from rest_framework_simplejwt.authentication import JWTAuthentication

class StudentApi(APIView):

    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student_obj = Student.objects.all()
        print("----------",request.user)
        serdata = StudentSerializer(student_obj,many=True).data
        return Response({'status':200,'data':serdata})

    def post(self, request):
        serializer = StudentSerializer(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

        serializer.save()
        return Response({'status':200,'data':serializer.data,'message':'your data is saved'})

    def put(self, request):
        try:
            studentobj = Student.objects.get(id=request.data['id'])

            serializer = StudentSerializer(studentobj,data = request.data,partial=False)

            if not serializer.is_valid():
                return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

            serializer.save()
            return Response({'status':200,'data':serializer.data,'message':'your data is updated'})   

        except Exception as e:
            return Response({'status':403,'message':'invalid id'})
        
    def patch(self,request):
        try:
            studentobj = Student.objects.get(id=request.data['id'])

            serializer = StudentSerializer(studentobj,data = request.data,partial=True)

            if not serializer.is_valid():
                return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

            serializer.save()
            return Response({'status':200,'data':serializer.data,'message':'your data is updated'})   

        except Exception as e:
            return Response({'status':403,'message':'invalid id'})
    
    def delete(self,request):
        try:
            id = request.GET.get('id')
            studentobj = Student.objects.get(id=id)
            studentobj.delete()
            return Response({'status':200,'message':'Deleted'}) 

        except Exception as e:
            print("e------------------------",e)
            return Response({'status':403,'message':'invalid id'})


############################ Session Authentication #########################

################ for jwt ###################################
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistration(APIView):

    def post(self,request):

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status':403,'errors':serializer.errors,'message':'something went wrong'})

        serializer.save()
        user = User.objects.get(username = serializer.data['username'])
        # token_obj , _ = Token.objects.get_or_create(user=user)

        ################ for jwt ###################################
        refresh = RefreshToken.for_user(user)

        # return Response({'status':200,'data':serializer.data,'token_obj':str(token_obj),'message':'your data is saved'})

        return Response({'status':200,
        'data':serializer.data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message':'your data is saved'})



############################ Generic Views  #########################

from rest_framework import generics

class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentGeneric1(generics.UpdateAPIView,generics.DestroyAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'