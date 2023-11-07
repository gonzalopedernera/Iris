from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class UserAccounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
def get_full_name(self):
    return self.name
def get_short_name(self):
    return self.name
def __str__(self):
    return self.email

def default_time():
    return {"08:00": True, "08:30": True, "09:00": True, "09:30": True, "10:00": True, "10:30": True, "11:00": True, "11:30": True, "12:00": True, "12:30": True, "13:00": False, "13:30": False, "14:00": True, "14:30": True, "15:00": True, "15:30": True, "16:00": True, "16:30": True, "17:00": True, "17:30": True, "18:00": True}
class Business_Data(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    name_business = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    social_media = models.CharField(max_length=100, default="Instagram")
    opening_hours = models.TimeField(default='08:00')
    closing_hours = models.TimeField(default='18:00')
    time_range = models.JSONField(default=default_time)
        
    def __str__(self):
        return self.name_business

class CollaboratorAccountManager(BaseUserManager):
    def create(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        collaborator = self.model(email=email, name=name, **extra_fields)
        collaborator.set_password(password)
        collaborator.save(using=self._db)
        return collaborator
class CollaboratorAccounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    id_business_data = models.ForeignKey(Business_Data, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CollaboratorAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='collaborator_accounts',
        blank=True,
        help_text='The groups this collaborator belongs to. A collaborator will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='collaborator_accounts',
        blank=True,
        help_text='Specific permissions for this collaborator.',
        verbose_name='user permissions',
    )
    def save(self, *args, **kwargs):
        created = not self.pk
        super(CollaboratorAccounts, self).save(*args, **kwargs)
        if created:
            # Si el colaborador es nuevo, va al grupo 'Collaborators'
            collaborator_group = Group.objects.get_or_create(name='Collaborators')[0]
            self.groups.add(collaborator_group)
            # Obtener el ContentType para el modelo de usuario personalizado
            content_type = ContentType.objects.get_for_model(Services)
            # Obtener los permisos para el modelo
            permissions = Permission.objects.filter(content_type=content_type)
            print([perm.codename for perm in permissions])
            print (type(permissions))
            # Convierte el queryset de permisos en una lista y asigna el conjunto de permisos al grupo
            for perm in list(permissions):
                collaborator_group.permissions.add(perm)
            # Convierte el queryset de permisos en una lista y asigna un permiso especifico al grupo
            #for perm in permissions:
            #   if perm.codename == "view_calendar":
            #       collaborator_group.permissions.add(perm)
    def __str__(self):
        return self.name

class Services(models.Model):
    id = models.AutoField(primary_key=True)
    #id_collaborator = models.ForeignKey(CollaboratorAccounts, on_delete=models.CASCADE)
    id_business_data = models.ForeignKey(Business_Data, on_delete=models.CASCADE)
    id_collaborator = models.ManyToManyField(CollaboratorAccounts)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=100)
    price = models.CharField(max_length=100)
    #duration = models.CharField(max_length=100, default='30')
    def __str__(self):
        return self.name

"""class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    id_business_data = models.ForeignKey(Business_Data, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    def __str__(self):
        return self.name"""

def validate_days(value):
    if value.weekday() == 5 or value.weekday() == 6:
        raise ValidationError("No se puede seleccionar un fin de semana")
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    id_service = models.ForeignKey(Services, on_delete=models.CASCADE)
    id_collaborator = models.ForeignKey(CollaboratorAccounts, on_delete=models.CASCADE)
    days = models.DateField(validators=[validate_days])
    startTime = models.TimeField(max_length=100, default='')
    name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=100, default='')
    def __str__(self):
        return f"Appointment {self.id}"
