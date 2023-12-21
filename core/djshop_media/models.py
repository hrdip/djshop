from django.db import models
import hashlib
from django.dispatch import receiver
from django.db.models.signals import pre_save
from . exceptions import DuplicateImageException

# file system, storage settings  in django 4.2 release (another choiceobject storage supported amazon S3)-> this type of storage suitable for uoloded files by client

class Image(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(width_field="width", height_field="height", upload_to="images/")
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)

    # hashing file
    file_hash = models.CharField(max_length=40, db_index=True, editable=False)
    file_size = models.PositiveIntegerField(null=True, editable=False)

    # focal points for image (witch part of picture is more important)((supported square or point or circle))
    # for point
    focal_points_x = models.PositiveIntegerField(null=True, blank=True)
    focal_points_y = models.PositiveIntegerField(null=True, blank=True)
    # for square
    focal_points_width = models.PositiveIntegerField(null=True, blank=True)
    focal_points_height = models.PositiveIntegerField(null=True, blank=True)

    # for set automatically file_hash and file_size fields
    def save(self,  *args, **kwargs):
        # before saving by super most be this to fields saved in
        self.file_size = self.image.size
        
        hasher = hashlib.sha1()
        for chunk in self.image.file.chunks():
            hasher.update(chunk)

        self.file_hash = hasher.hexdigest()

        super().save(*args, **kwargs)


# same hash checking obj befor saving and raise exception
# use signal with receiver
@receiver(pre_save, sender=Image)
def check_duplicate_hash(sender, instance, **kwargs):
    existed = Image.objects.filter(file_hash=instance.file_hash).exclude(pk=instance.pk).exists()
    if existed:
        raise DuplicateImageException("Duplicate")
