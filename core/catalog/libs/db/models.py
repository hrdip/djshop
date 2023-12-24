from django.db import models
from django.conf import settings


# abstract model

class AuditableModel(models.Model):
    # we want custom User then we are not using auth model of django the use settings
    # we need only app label and model name but if you need User class most use this function( get_user_model())
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True, related_name='created')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.SET_NULL, null=True, related_name='modified')
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    # use abstract model like this
    class Meta:
        abstract = True