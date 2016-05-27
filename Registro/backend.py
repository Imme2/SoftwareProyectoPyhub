# from Registro.models import usuario
# 
# class usuarioAuth(object):
# 
#     def authenticate(self, username=None, password=None):
#         try:
#             user = usuario.objects.get(username=username)
# 
#             if password == user.clave:
#                 # Authentication success by returning the user
#                 return user
#             else:
#                 # Authentication fails if None is returned
#                 return None
#         except usuario.DoesNotExist:
#             return None
# 
#     def get_user(self, user_id):
#         try:
#             return usuario.objects.get(pk=user_id)
#         except usuario.DoesNotExist:
#             return None