import django_filters
from django.db.models import F, Avg
from django.shortcuts import redirect
from django.http import HttpResponse
from rest_framework import viewsets, serializers, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, Category, SubTask
from .serializers import UserSerializer, SubTaskSerializer, TaskSerializer, CategorySerializer
from auth_service.serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


def todolist(request):
    return HttpResponse('todolist')


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ['priority']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['priority']


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer


def redirect_view(request):
    return redirect("/category")  # редирект с главной на категории


class MergeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = UserSerializer(many=True, read_only=True)
    count_tasks = serializers.IntegerField()

    class Meta:
        model = Task
        fields = '__all__'


@api_view(['GET'])
def statistics_users(request):
    tasks = Task.objects
    if 'user' in request.GET:
        tasks = tasks.filter(user=request.GET['user'])
    if 'username' in request.GET:
        tasks = tasks.filter(user__username=request.GET['username'])

    if 'category_id' in request.GET:
        tasks = tasks.filter(user=request.GET['category_id'])

    avg_times = tasks.annotate(tdiff=(F('due_date') - F('created'))).values('tdiff').annotate(
        avg_time=Avg('tdiff')).values('avg_time', 'user')

    return Response({
        "count_task": tasks.count(),
        "finished_tasks": tasks.filter(done=1).count(),
        "unfinished_tasks": tasks.filter(done=0).count(),
        "avg_times": avg_times
    })
