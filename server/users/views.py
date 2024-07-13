# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
import logging
from django.http import JsonResponse
from django.middleware.csrf import get_token
import json
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .models import Interest, Chat
from .serializers import InterestSerializer, ChatSerializer
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CustomUserCreationForm(data)
            if form.is_valid():
                user = form.save()
                logger.info(f"User {user.username} registered successfully.")
                login(request, user)
                return JsonResponse({'message': 'Registration successful'}, status=200)
            else:
                logger.error("Form is not valid.")
                logger.error(form.errors)
                return JsonResponse({'error': form.errors}, status=400)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("Error decoding JSON or missing key.")
            logger.error(e)
            return JsonResponse({'error': 'Invalid data'}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            password = data['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

def home(request):
    return render(request, 'users/home.html')

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    users = User.objects.all().values('id', 'username', 'email')
    return Response(users)


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['sender'] = request.user.id  # Set the sender as the current logged-in user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(receiver=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.receiver == request.user:
            instance.status = request.data.get('status', instance.status)
            instance.save()
            return Response({'status': 'Interest updated'})
        return Response({'error': 'Not authorized'}, status=403)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        interest = self.get_object()
        if interest.receiver == request.user:
            interest.status = 'accepted'
            interest.save()
            return Response({'status': 'Interest accepted'})
        return Response({'error': 'Not authorized'}, status=403)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        interest = self.get_object()
        if interest.receiver == request.user:
            interest.status = 'rejected'
            interest.save()
            return Response({'status': 'Interest rejected'})
        return Response({'error': 'Not authorized'}, status=403)
    
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(sender=user) | Chat.objects.filter(receiver=user)    
