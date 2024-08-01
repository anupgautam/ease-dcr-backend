import jwt
from DCR.settings import SECRET_KEY
def get_user_from_access(access):
    try:
        decrypted_access_token = jwt.decode(
                                access,
                                SECRET_KEY,
                                algorithms=['HS256'])
        user_id = int(decrypted_access_token.get('user_id'))
        return user_id
    except Exception as e:
        raise Exception('Invalid access token')