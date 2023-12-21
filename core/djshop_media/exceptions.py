from rest_framework.exceptions import APIException

# business exception

# prevent uploading the duplicated image

# overwrite this class
class DuplicateImageException(APIException):
    pass
