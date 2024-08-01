from utility.constants import IMAGE_EXTENSIONS
def check_image_extension(data):
    for i in IMAGE_EXTENSIONS:
        if(data.__contains__(i)):
            return True
    return False