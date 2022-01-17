import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import jwt


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)

    @property
    def token(self):
        token = jwt.encode(
            {'username': self.username, 'userId': str(self.id), 'exp': datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY, algorithm='HS256')
        return token
