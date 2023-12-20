from django.db import models


# custom field (over write)
# get any data and save uppercase in db and if data saved in db is lowercase change it to uppercase
class UpercasesCharField(models.CharField):
    

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)
    
    def to_python(self, value):
        val = super().to_python(value)
        if isinstance(val, str):
            return val.upper()
        return val