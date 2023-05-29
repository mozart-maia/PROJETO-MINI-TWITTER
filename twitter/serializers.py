from django.contrib.auth.models import User, Group
from rest_framework import serializers
from twitter.models import Publicacao

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Ja existe um usuario com esse login!')
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(first_name = validated_data['first_name'], last_name =validated_data['last_name'], username = validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return validated_data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Conta não encontrada')
        
        return data
    
    def get_jwt_token(self, data):

        user = authenticate(username= data['username'], password = data['password'])

        if not user :
            return {'message': 'credenciais inválidas' , 'data' : {"Login ou senha não correspondem"}}
        
        refresh = RefreshToken.for_user(user)

        return {'message': 'login efetuado com sucesso', 'data': {'token' : { 'refresh': str(refresh), 'access' : str(refresh.access_token) }}}

class PublicacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacao
        fields = ['id', 'conteudo', 'data_criacao', 'autor']
    autor = serializers.ReadOnlyField(source='autor.username')
    
    
    # id = serializers.IntegerField(read_only=True)
    # conteudo = serializers.CharField(max_length=280, allow_blank=True, required=False)
    # usuario = serializers.CharField(max_length=50, required=False)

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Publicacao` instance, given the validated data.
    #     """
    #     return Publicacao.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Publicacao` instance, given the validated data.
    #     """
    #     instance.conteudo = validated_data.get('conteudo', instance.conteudo)
    #     instance.usuario = validated_data.get('usuario', instance.usuario)
    #     instance.save()
    #     return instance