# login_usuario/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tenta encontrar um usuário que corresponda ao email OU ao nome de usuário.
            # O 'iexact' faz a busca ser case-insensitive (ignora maiúsculas/minúsculas).
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Se nenhum usuário for encontrado, a autenticação falha.
            return None
        
        # Se um usuário foi encontrado, verifica a senha dele.
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        # Se a senha estiver incorreta, a autenticação falha.
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None