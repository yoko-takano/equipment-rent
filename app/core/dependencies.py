from app.persistence.auth_persistence import AuthPersistence
from app.persistence.user_persistence import UserPersistence
from app.services.auth_service import AuthService
from app.services.user_service import UserService


def inject_dependencies():
    AuthService(AuthPersistence)
    UserService(UserPersistence)
    AuthService(AuthPersistence)
