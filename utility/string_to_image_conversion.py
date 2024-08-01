from abc import ABC, abstractmethod
from utility.base64Converter import decode_base64_file
from utility.urlConvertImage import url_to_image
from utility.constants import BASE_URL
from utility.check_image_extension import check_image_extension
class FileConversion(ABC):
    @abstractmethod
    def convert():
        pass
class Base64ToImageConversion(FileConversion):
    def __init__(self, base64File):
        self.base64File = base64File
    def convert(self):
        return decode_base64_file(self.base64File)
class URLToImageConversion(FileConversion):
    def __init__(self, url):
        self.url = url
    def convert(self):
        return url_to_image(self.url)
def image_conversion(validated_data):
    keys = validated_data.keys()
    for k in keys:
        if isinstance(validated_data[k], str):
            if isinstance(validated_data[k], str) and validated_data[k].__contains__('base64'):
                validated_data[k] = Base64ToImageConversion(validated_data[k]).convert()
            elif isinstance(validated_data[k], str) and check_image_extension(validated_data[k]):
                if validated_data[k].__contains__('http'):
                    validated_data[k] = URLToImageConversion(validated_data[k]).convert()
                else:
                    validated_data[k] = URLToImageConversion(BASE_URL+validated_data[k]).convert()
            else:
                validated_data[k] = validated_data[k]
        elif isinstance(validated_data[k], list):
            for l in validated_data[k]:
                for key , value in l.items():
                    if isinstance(value, str) and value.__contains__('base64'):
                        l[key] = Base64ToImageConversion(value).convert()
                    elif isinstance(value, str) and check_image_extension(value):
                        l[key] = URLToImageConversion(value).convert()
                    else:
                        l[key] = value
    return validated_data







