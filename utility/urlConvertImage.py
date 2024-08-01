import requests
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import imghdr
import uuid
from utility.base64Converter import get_file_extension
# Download the image data from the URL
def url_to_image(url):
    image_url = url
    response = requests.get(image_url)
    image_data = response.content
    # Create a BytesIO object to store the image data in memory
    file = BytesIO(image_data)
   # Determine the image format
    image_format = imghdr.what(file)
    # Use the image format to determine the content type
    if image_format == 'jpeg':
        content_type = 'image/jpeg'
    elif image_format == 'png':
        content_type = 'image/png'
    elif image_format == 'gif':
        content_type = 'image/gif'
    else:
        content_type = 'application/octet-stream'
    file.seek(0)
    # Create an InMemoryUploadedFile object
            # Generate file name:
    file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
    image = InMemoryUploadedFile(
        file, None, 'image.jpg', content_type, len(image_data), None)
    return image









