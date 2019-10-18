from werkzeug.wsgi import ClosingIterator


class AfterResponse:
    '''App extension which wraps the middleware
    '''
    def __init__(self, app):
        self.callbacks = []
        
        # install extension
        app.after_response = self
        
        # install middleware
        app.wsgi_app = AfterResponseMiddleware(app.wsgi_app, self)

    def __call__(self, callback):
        self.callbacks.append(callback)
        return callback

    def flush(self):
        for fn in self.callbacks:
            fn()

class AfterResponseMiddleware:
    '''WSGI middleware to return `ClosingIterator` with callback functions
    '''
    def __init__(self, application, after_response_ext):
        self.application = application
        self.after_response_ext = after_response_ext

    def __call__(self, environ, after_response):
        iterator = self.application(environ, after_response)
        try:
            return ClosingIterator(iterator, [self.after_response_ext.flush])
        except:
            return iterator
