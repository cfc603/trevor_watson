from .models import BusinessView


class ViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # does request have business key
        BusinessView.create_from_request(request)
        response = self.get_response(request)
        return response
