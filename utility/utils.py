import requests
import uuid

from rest_framework.permissions import (AllowAny)
from bs4 import BeautifulSoup

from .constants import NMC_URL


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in
    view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False

# validating nmc no of the doctors in dental app

def nmc_no_validation(nmc_no: int) -> bool:
    my_html_doc = requests.get('{nmc_url}?name=&nmc_no={nmc_no}&degree='
                    .format(nmc_url=NMC_URL, nmc_no=nmc_no))
    soup = BeautifulSoup(my_html_doc.content, 'html.parser')
    for data in soup.find_all('td'):
        if data.string == str(nmc_no):
            return True
    return False

# frequently used serializer save method

def serializer_save(className, data):
    
    # data['id'] = str(data.get('id'))
    
    serializer = className.serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    
    serializer.save()
    
    return serializer

# generate 8 bit uuid 
def get_8_bit_uuid():
    full_uuid = uuid.uuid4()
    return full_uuid