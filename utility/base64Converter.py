from PIL import Image
from io import BytesIO
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import six
import uuid
import imghdr
def get_file_extension(file_name, decoded_file):
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension
def find_base64_fields(data, index=[]):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                find_base64_fields(value, index)
            elif isinstance(value, str) and value.__contains__('base64'):
                index.append(key)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                find_base64_fields(item, index)
            elif isinstance(item, str) and item.__contains__('base64'):
                index.append(i)
    return index
def decode_base64_file(data):
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')
        # Try to decode the file. Return validation error if it fails.
        try:
            data.rstrip('=')
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')
        # Generate file name:
        file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)
        complete_file_name = "%s.%s" % (file_name, file_extension, )
        content = ContentFile(decoded_file, name=complete_file_name)
        return InMemoryUploadedFile(content, None, complete_file_name, 'image/jpeg', len(decoded_file), None)







