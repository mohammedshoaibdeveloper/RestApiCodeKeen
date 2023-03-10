from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from .models import *
from.serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
import Api.faker as fake
from Api.helper import *




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


@api_view(['GET'])
def generatedata(request):

    fake.generate_random_data()
    return Response({'status':200})
import datetime

class GeneratePdf(APIView):
    def get(self, request):

        studentObj = Student.objects.all()
        params = {
            'today': datetime.datetime.today(),
            'student_obj':studentObj
        }
        filename,status = pdf.save_pdf(params)
        if not status:

            return Response({'status':400})

        return Response({'status':200,'path':f'/media/{filename}.pdf'})

import pandas as pd
from django.conf import settings
import uuid

class ExporImportExcel(APIView):

    def get(self, request):
        student_obj = Student.objects.all()
        serializer = StudentSerializer(student_obj,many=True)

        df = pd.DataFrame(serializer.data)
        print(df)
        df.to_csv(f"public/static/excel/{uuid.uuid4}.csv",encoding="UTF-8",index=False)
        return Response({"status":200})

    def post(self,request):

        excel_upload_obj = Excelfileuupload.objects.create(excel_file_upload = request.FILES['files'])
        df  = pd.read_csv(f"{settings.BASE_DIR}/public/static/{excel_upload_obj.excel_file_upload}")
        for student in (df.values.tolist()):
            print(student)


        return Response({"status":200})



class RegisterView(APIView):
    
    def post(self, request):

        try:

            serializer = CustomeUserSerializer(data = request.data)
            if not serializer.is_valid():

                return Response({"status":403,'errors':serializers.errors})

            serializer.save()
            return Response({"status":200,"message":"en email OTP  send on your number and email"})

        
        except Exception as e:

            print(e)
            return Response({'status':404,'errors':'something went wrong'})


class VerifyOtp(APIView):

    def post(self, request):
        try:
            data  = request.data
            user_obj = User.objects.get(phone = data.get('phone'))
            otp = data.get('otp')
            if user_obj.otp == otp:
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({"status":200,"message":"your otp is verified"})

            return Response({"status":403,"message":"your otp is wrong"})
        except Exception as e:
            print(e)
            return Response({'status':404,'errors':'something went wrong'})

    
    def patch(self, request):

        try:
            data  = request.data
            user_obj = User.objects.filter(phone = data.get('phone'))

            if not user_obj.exists():
                return Response({'status':404,'errors':'no user found!'})

            status,time = send_otp_mobile(data.get('phone'),user_obj[0])
            if status:
                return Response({'status':200,'message':'new otp sent'})

            return Response({'status':404,'errors':f'try after few seconds {time}'})

        except Exception as e:
            print(e)
            return Response({'status':404,'errors':'something went wrong'})
