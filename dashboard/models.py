import uuid
from django.db import models
from django.conf import settings


# Create your models here.

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,unique=True, null = False, editable=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE,blank = True)
    name = models.CharField(max_length=50, verbose_name="profile name", null=True, blank = True)
    phone = models.IntegerField(verbose_name="Phone number", 
                                null=True, default=None, blank=True)
    born_date = models.DateField(verbose_name="Born date" , null=True,
                                default=None, blank=True)
    email = models.EmailField()
    profile_pic = models.ImageField(blank = True)
    location = models.CharField(max_length=100, null=True,blank=True)
    city = models.CharField(max_length=100, null=True,blank=True)
    state = models.CharField(max_length=100, null=True,blank=True)

    class Meta:
        verbose_name = 'profile'

    def __str__(self):
        return self.name or self.email

    @property
    def picture_url(self):
        return self.profile_pic.url
    



