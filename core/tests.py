from django.test    import TestCase
from django.utils   import timezone

from .models import User, Task


class TestUserModel(TestCase):
    """ 
    TestUserModel class for testing User model
    """
    def setUp(self):
        """
        setUp method for creating test data
        """
        self.tasks = [
            {
                "name": "test task"
            },
            {
                "name": "test task 2",
                "description": "test task description2",
                "is_completed": True,
            },
            {
                "name": "test task 3",
                "description": "test task description3",
                "begin_at": timezone.now(),
                "end_at": None,
            },
            {
                "name": "test task 4",
                "description": None,
                "begin_at": timezone.now() - timezone.timedelta(days=1),
                "end_at": timezone.now() + timezone.timedelta(microseconds=1)
            },
        ]
        
        self.user = User.objects.create_user(
            username="testuser",
            email="s@s.com",
            password="testpass",
            first_name="test",
            last_name="user",
        )
        
        self.user.create_task(**self.tasks[0])
        self.user.create_tasks(self.tasks[1:])
    
    def test_create_task_model_with_user(self):
        # test create task with user
        task = self.user.get_task(name = "test task")
        self.assertEqual(task.name, "test task")
        self.assertEqual(task.created_by, self.user)
        self.assertEqual(task.is_completed, False)
        self.assertAlmostEqual(task.begin_at, timezone.now(), delta=timezone.timedelta(seconds=1))
        self.assertEqual(task.end_at, None)
        self.assertLess(task.created_at, task.updated_at)
        
        task2 = Task.objects.get(name="test task 2")
        self.assertEqual(task2.description, "test task description2")
        
    def test_user_get_task_method(self):
        """ test get task method of user """
        task = self.user.get_task(id = 1)
        self.assertEqual(task.name, "test task")
        
        task = self.user.get_task(name = "test task 2")
        self.assertEqual(task.name, "test task 2")
        
        task = self.user.get_task(description = "test task description3")
        self.assertEqual(task.name, "test task 3")
        
        task = self.user.get_task(begin_at__lte = timezone.now() + timezone.timedelta(hours = -10))
        self.assertEqual(task.name, "test task 4")
        
    def test_user_get_all_tasks_method(self):
        # test get all tasks method of user
        tasks = self.user.get_tasks()
        
        self.assertEqual(len(tasks), len(self.tasks))
        self.assertListEqual(
            sorted([task.name for task in tasks]),
            sorted([task["name"] for task in self.tasks])
        )
        
    def test_user_get_completed_tasks_method(self):
        # test get completed tasks method of user
        tasks = self.user.get_completed_tasks()
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, "test task 2")
        
    def test_user_get_active_tasks_method(self):
        # test get active tasks method of user
        tasks = self.user.get_active_tasks()
        
        self.assertListEqual(
            sorted([task.name for task in tasks]),
            sorted([task["name"] for task in [self.tasks[0]] + [self.tasks[2]]])
        )
        
    def test_user_update_task_method(self):
        """ test update task method of user """
        task = self.user.update_task(id = 1, name = "test task updated", description = "test task description updated")
        self.assertEqual(task.name, "test task updated")
        self.assertEqual(task.description, "test task description updated")
        
    def test_user_update_tasks_method(self):
        """ test update tasks method of user """
        tasks = self.user.update_tasks(ids = [1, 3, 4], is_completed = True)
        
        self.assertEqual(tasks, 3)
        tasks = self.user.get_completed_tasks()
        self.assertEqual(len(tasks), 4)
        
    def test_user_complete_task_method(self):
        """ test complete task method of user """
        task = self.user.complete_task(id = 1)
        self.assertEqual(task.is_completed, True)
    
    def test_user_complete_tasks_method(self):
        """ test complete tasks method of user """
        tasks = self.user.complete_tasks(ids = [1, 3, 4])
        self.assertEqual(tasks, 3)
        
        tasks = self.user.get_completed_tasks()
        self.assertEqual(len(tasks), 4)
        
    def test_user_incomplete_task_method(self):
        """ test incomplete task method of user """
        task = self.user.incomplete_task(id = 2)
        self.assertEqual(task.is_completed, False)
        
    def test_user_incomplete_tasks_method(self):
        """ test incomplete tasks method of user """
        tasks = self.user.incomplete_tasks(ids = [1, 3, 4])
        self.assertEqual(tasks, 3)
        
        tasks = self.user.get_completed_tasks()
        self.assertEqual(len(tasks), 1)
    
    def test_user_delete_task_method(self):
        """ test delete task method of user """
        task = self.user.delete_task(id = 1)
        self.assertEqual(task.name , "test task")
        
        tasks = self.user.get_tasks()
        self.assertEqual(len(tasks), 3)
        
    def test_user_delete_tasks_method(self):
        """ test delete tasks method of user """
        tasks = self.user.delete_tasks(ids = [1, 3, 4])
        self.assertEqual(tasks, 3)
        
        tasks = self.user.get_tasks()
        self.assertEqual(len(tasks), 1)
    
    