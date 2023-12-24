from django.db import models
from django.contrib.admin.models import LogEntry


# in proxy model we cant change te filed and we just over write the class 

# if you want tracking user to know how they use our system
class FootPrint(models.Model):
    pass

# we want over write (log entries) used for keeping history logings in admin
class ActionHistory(LogEntry):
    class Meta:
        proxy = True