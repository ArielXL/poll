from threading import current_thread

from django.utils.deprecation import MiddlewareMixin

_requests = {}


def current_request():
    return _requests.get(current_thread().ident, None)


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _requests[current_thread().ident] = request

    def process_response(self, request, response):
        # when response is ready, request should be flushed
        _requests.pop(current_thread().ident, None)
        return response

    def process_exception(self, request, exception):
        # if an exception has happened, request should be flushed too
        _requests.pop(current_thread().ident, None)


def doc_model_view(app_name, model_name_singular, model_name_plural):
    def handler(self):
        self.__doc__ = f"""
        {app_name.upper()}
        -----------------------
        ### {model_name_singular.capitalize()} model. \n
        
        GET
        ---
            Shows all {model_name_plural.lower()} created. \n
        POST
        ----
            Adds a new {model_name_singular.lower()}. \n
        GET/{'{'}id{'}'}
        -------
            Retrieves a specific {model_name_singular.lower()} determined by id. \n
        PUT/{'{'}id{'}'}
        -------
            Modifies all fields of a specific {model_name_singular.lower()} determined by id. \n
        PATCH/{'{'}id{'}'}
        ---------
            Partially modifies the fields of a specific {model_name_singular.lower()} determined by id. \n
        DELETE/{'{'}id{'}'}
        ----------
            Deletes a specific {model_name_singular.lower()} determined by id. \n
        """

        return self

    return handler
