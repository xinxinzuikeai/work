# coding:utf8

# django1.8没有MiddlewareMixin这个类,所以这里需要自己写一个类
class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

# 这里是自定义的中间件类
class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print "中间件:",request.GET.get('a')