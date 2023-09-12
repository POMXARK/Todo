import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from todolist.models import Category, Task, SubTask
from todolist.serializers import CategorySerializer, TaskSerializer, SubTaskSerializer
from rest_framework.test import APIClient

from todolist.views import MergeSerializer

client = APIClient()


class AccountTests(APITestCase):

    def setUp(self):
        self.maxDiff = None

        url = reverse('auth_register')
        data = {
            "username": "superadmin",
            "email": "admin@admin.com",
            "first_name": "superadmin",
            "last_name": "superadmin",
            "password": "superadmin",
            "password2": "superadmin"
        }

        response = client.post(url, data, format='json')
        try:
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            print(response.data)

    def test_create_category(self):
        url = reverse('categories-list')
        client.post(url, {'name': 'test'}, format='json')
        instance = Category.objects.first()
        serializer = CategorySerializer(instance)
        self.assertEqual(serializer.data, {'id': 1, 'name': 'test'})

    def test_create_task(self):
        self.test_create_category()
        url = reverse('tasks-list')
        data = {
            "title": "test_task",
            "description": "any",
            "priority": 1,
            "created": '2023-01-01',
            "due_date": '2023-01-02',
            "done": False,
            "category": 1,
            "user": [1]
        }
        response = client.post(url, data, format='json')
        try:
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            print(response.data)
        instance = Task.objects.first()
        serializer = TaskSerializer(instance)
        self.assertEqual(serializer.data['title'], 'test_task')

    def test_create_subtask(self):
        self.test_create_task()
        url = reverse('subtasks-list')
        data = {
            "title": "test_subtask",
            "description": "any",
            "created": '2023-01-01',
            "due_date": '2023-01-02',
            "task": 1,
        }
        response = client.post(url, data, format='json')
        try:
            self.assertEqual(response.status_code, 201)
        except AssertionError:
            print(response.data)
        instance = SubTask.objects.first()
        serializer = SubTaskSerializer(instance)
        self.assertEqual(serializer.data['title'], 'test_subtask')

    def test_filter_and_ordering_task_by_priority(self):
        self.test_create_task()
        url = reverse('tasks-list')
        response = client.get(url + '?ordering=priority&priority=1', {}, format='json')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            print(response.data)
        serializer = TaskSerializer(response.data)
        self.assertEqual(serializer.instance[0]['priority'], 1)

    def test_update_subtask(self):
        self.test_create_subtask()
        url = reverse('subtasks-list')
        data = {
            "title": "test_subtask_updated",
            "description": "any",
            "created": '2023-01-01',
            "due_date": '2023-01-02',
            "task": 1,
        }
        response = client.put(url + '1/', data, format='json')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            print(response.data)
        instance = SubTask.objects.first()
        serializer = SubTaskSerializer(instance)
        self.assertEqual(serializer.data['title'], 'test_subtask_updated')

    def test_delete_subtask(self):
        self.test_create_subtask()
        url = reverse('subtasks-list')
        response = client.delete(url + '1/')
        try:
            self.assertEqual(response.status_code, 204)
        except AssertionError:
            print(response.data)
        instance = SubTask.objects.first()
        serializer = SubTaskSerializer(instance)
        self.assertEqual(serializer.data['title'], '')

    def test_statistics(self):
        self.test_update_subtask()
        url = reverse('statistics-users')
        response = client.get(url + '?user=1&username=superadmin&category_id=1', {}, format='json')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError:
            print(response.data)
        serializer = MergeSerializer(response.data)
        self.assertEqual(serializer.instance['count_task'], 1)
        self.assertEqual(serializer.instance['finished_tasks'], 0)
        self.assertEqual(serializer.instance['unfinished_tasks'], 1)
        self.assertEqual(serializer.instance['avg_times']._result_cache, [{'user': 1, 'avg_time': datetime.timedelta(days=1)}])