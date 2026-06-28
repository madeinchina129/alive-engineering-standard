```python
# JWT 认证示例
import jwt
from datetime import datetime, timedelta

class AuthService:
    SECRET_KEY = os.environ['JWT_SECRET']
    ACCESS_TOKEN_EXPIRE = timedelta(hours=2)
    REFRESH_TOKEN_EXPIRE = timedelta(days=7)
    
    def create_tokens(self, user_id: str, roles: list[str]) -> dict:
        now = datetime.utcnow()
        access_payload = {
            'sub': user_id,
            'roles': roles,
            'type': 'access',
            'iat': now,
            'exp': now + self.ACCESS_TOKEN_EXPIRE
        }
        refresh_payload = {
            'sub': user_id,
            'type': 'refresh',
            'iat': now,
            'exp': now + self.REFRESH_TOKEN_EXPIRE
        }
        return {
            'access_token': jwt.encode(access_payload, self.SECRET_KEY, algorithm='HS256'),
            'refresh_token': jwt.encode(refresh_payload, self.SECRET_KEY, algorithm='HS256')
        }
    
    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthException('Token 已过期')
        except jwt.InvalidTokenError:
            raise AuthException('无效的 Token')
```