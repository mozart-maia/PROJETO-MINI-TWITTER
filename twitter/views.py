from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import permissions, status
from twitter.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser
from twitter.models import Publicacao
from twitter.serializers import PublicacaoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Alguma coisa deu errado',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                    'data': {},
                    'message': 'Sua conta foi criada',
                }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                    'data': {},
                    'message': 'Alguma coisa deu errado',
                }, status=status.HTTP_400_BAD_REQUEST) 

class LoginView(APIView):


    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'credenciais invalidas'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)
            return Response(response, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': 'alguma coisa deu errado'
                }, status = status.HTTP_400_BAD_REQUEST)

class PubList(generics.ListCreateAPIView):
    queryset = Publicacao.objects.all()[:10]
    serializer_class = PublicacaoSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class PubDetalhe(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Publicacao.objects.all()
    serializer_class = PublicacaoSerializer

class AdicionarPub(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

    def post(self, request):
        try:
            data = request.data
            print(request.user)
            print(data)
            # data['autor'] = request.user
            serializer = PublicacaoSerializer(data = data)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Erro na requisicao post -Criar tweet-'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Tweet criado'
            }, status=status.HTTP_201_CREATED)


        except Exception as e:
            print(e)
            return Response({
                    'data': serializer.errors,
                    'message': 'Erro na requisicao post -Criar tweet-'
                }, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
# def list_pub(request):
#     if request.method == 'GET':
#         pubs = Publicacao.objects.all()
#         serializer = PublicacaoSerializer(pubs, many=True)
#         print(JsonResponse(serializer.data, safe=False))
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PublicacaoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
    

# @csrf_exempt
# def pub_detalhe(request, pk):
#     try:
#         pub = Publicacao.objects.get(pk=pk)
#     except Publicacao.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PublicacaoSerializer(pub)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = PublicacaoSerializer(pub, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         pub.delete()
#         return HttpResponse(status=204)