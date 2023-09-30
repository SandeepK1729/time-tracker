from django.db import models

from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail

from .exceptions import TaskNotFoundException

sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username        = models.CharField(
                        _("Username"),
                        max_length=150,
                        unique=True,
                        help_text=_(
                            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
                        ),
                        validators=[username_validator],
                        error_messages={
                            "unique": _("A user with that username already exists."),
                        },
                    )
    password        = models.CharField(_("password"), max_length=128)
    first_name      = models.CharField(_("first name"), max_length=150, blank=True)
    last_name       = models.CharField(_("last name"), max_length=150, blank=True)
    email           = models.EmailField(_("email address"), blank=True)
    gender      = models.CharField(
                    max_length=50, 
                    choices=sex_choice, 
                    default='Male'
                )
    date_joined     = models.DateTimeField(_("date joined"), default=timezone.now)
    is_staff        = models.BooleanField(
                        _("staff status"),
                        default = False,
                    )
    is_active       = models.BooleanField(
                        _("active"),
                        default = True,
                    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.username} - {self.first_name} {self.last_name}"

    def get_all_groups(self):
        return self.groups

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class User(AbstractUser):
    # CustomUser model will be act as General class of parent

    # Create or Insert of tasks
    def create_task(self, **kwargs):
        """ create task of user

        Returns:
            Task: Task object
        """
        return self.tasks.create(**kwargs)
    
    def create_tasks(self, tasks):
        """ create tasks of user
        
        Args:
            List[Dict]: List of tasks
        Returns:
            List[Task]: List of Task objects
        """
        return self.tasks.bulk_create([
                Task(**task, created_by=self) for task in tasks
            ])

    # Read or Retrieve of tasks
    def get_task(self, **args):
        """ get task of user

        Returns:
            Task: Task object
        """
        try:
            return self.tasks.get(**args, created_by=self)
        except Task.DoesNotExist:
            raise TaskNotFoundException(args)
        
    def get_tasks(self, **args):
        """ get all tasks of user

        Returns:
            Queryset: Queryset of tasks
        """
        return self.tasks.all().filter(**args).order_by(
                '-created_at'
            ).select_related(
                'created_by'
            )
    
    def get_completed_tasks(self):
        """ get all completed tasks of user

        Returns:
            Queryset: Queryset of completed tasks
        """
        return self.tasks.filter(
                is_completed=True
            ).order_by(
                '-created_at'
            ).select_related(
                'created_by'
            )
    
    def get_active_tasks(self):
        """ get all active tasks of user

        Returns:
            Queryset: Queryset of active tasks
        """
        
        return self.tasks.filter(
                is_completed=False
            ).filter(
                begin_at__lte=timezone.now()
            ).filter(
                models.Q(end_at__gte=timezone.now()) | models.Q(end_at__isnull=True)
            ).filter(
                is_completed = False
            ).order_by(
                '-created_at'
            ).select_related(
                'created_by'
            )

    # Update of tasks
    def update_task(self, id : int, **kwargs):
        """ update task of user

        Args:
            self (User): current user
            id (int): task id
            **args (dict): task fields
            
        Returns:
            Task: Task object
        """
        task = self.get_tasks(id = id)
        task.update(**kwargs)
        return task.first()
    
    def update_tasks(self, ids: list[int] = [], **args):
        """ update tasks of user
        
        Args:
            self (User): current user
            ids (List[int]): list of task ids
            **args (dict): task fields
            
        Returns:
            int: number of updated tasks
        """
        return self.tasks.filter(id__in = ids).filter(created_by = self).update(**args)

    def complete_task(self, id: int):
        """ complete task of user

        Args:
            self (User): current user
            id (int): task id

        Raises:
            TaskNotFound: if task not found

        Returns:
            Task : Task object
        """
        self.update_task(id = id, is_completed = True)
        return self.get_task(id = id)
    
    def complete_tasks(self, ids: list[int] = []):
        """ complete tasks of user
        
        Args:
            self (User): current user
            ids (List[int]): list of task ids
            
        Returns:
            int: number of completed tasks
        """
        return self.update_tasks(ids = ids, is_completed = True)
    
    def incomplete_task(self, id: int):
        """ incomplete task of user
        
        Args:
            self (User): current user
            id (int): task id
            
        Returns:
            Task: Task object
        """
        task = self.update_task(id = id, is_completed = False)
        return task
    
    def incomplete_tasks(self, ids: list[int] = []):
        """ incomplete tasks of user
        
        Args:
            self (User): current user
            ids (List[int]): list of task ids
            
        Returns:
            int: number of incomplete tasks
        """
        return self.update_tasks(ids = ids, is_completed = False)
    
    def delete_task(self, id: int):
        """ delete task of user
        
        Args:
            self (User): current user
            id (int): task id
            
        Returns:
            Task: Task object
        """
        task = self.get_task(id = id)
        task.delete()
        return task
    
    def delete_tasks(self, ids: list[int] = []):
        """ delete tasks of user
        
        Args:
            self (User): current user
            ids (List[int]): list of task ids
            
        Returns:
            int: number of deleted tasks
        """
        return self.tasks.filter(id__in = ids, created_by = self).delete()[0]
    
class Task(models.Model):
    """
    Task model for storing task information
    """
    name            = models.CharField(max_length=100, db_index=True)
    description     = models.TextField(null=True, blank=True)
    created_by      = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'tasks')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    is_completed    = models.BooleanField(default=False)
    begin_at        = models.DateTimeField(default=timezone.now, db_index=True)
    end_at          = models.DateTimeField(blank=True, null=True, default=None, db_index=True)
    
    def save(self, *args, **kwargs):
        """Override save method of task model to set begin_at and end_at field"""
        if self.end_at is not None and self.begin_at > self.end_at:
            raise ValueError("begin_at must be less than or equal to end_at")
        
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Generate string representation of task

        Returns:
            str : String representation of task object, ex : Task 1 created by user1 active from 2021-08-01 00:00:00 to 2021-08-31 00:00:00
        """
        return f"{self.name} created by {self.created_by} active from {self.begin_at} to {self.end_at}"
    
    @property
    def duration(self):
        """Calculate duration of task

        Returns:
            timedelta : Duration of task
        """
        return self.end_at - self.begin_at
    