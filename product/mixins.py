

class ProductUserMixin():
    
    def post(self, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        msg = f'{obj} was deleted by {user}'
        sys_loggin('info', True, msg)
        return super().post(*args, **kwargs)