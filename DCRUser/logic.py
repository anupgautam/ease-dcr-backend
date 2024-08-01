import jwt
import string
import random

from DCR.settings import SECRET_KEY
from DCRUser.models import CompanyUser
from DCRUser.models import CompanyUserRole


## characters to generate password from
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate_random_password():
	## length of password from the user
	## shuffling the characters
	random.shuffle(characters)
	
	## picking random characters from the list
	password = []
	for i in range(10):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## returing the list
	return("".join(password))


def get_user_from_access(access):
		decrypted_access_token = jwt.decode(
									access,
									SECRET_KEY,algorithms=['HS256'])
		user_id = decrypted_access_token.get('user_id')
		company_data ={
		'company_name' : CompanyUser.objects.get(user_name=user_id).company_name.company_id,
		'company_address' : CompanyUser.objects.get(user_name=user_id).company_name.company_address,
		'company_email_address' : CompanyUser.objects.get(user_name=user_id).company_name.company_email_address
		}
		return company_data

def get_role_from_access(access):
	decrypted_access_token = jwt.decode(
									access,
									SECRET_KEY,algorithms=['HS256'])
	user_id = decrypted_access_token.get('user_id')
	instance = CompanyUserRole.objects.get(user_name__id=user_id)
