from unittest.mock import Mock, patch

from django.test import TestCase

from ..middleware import ViewTrackingMiddleware


class ViewTrackingMiddlewareTest(TestCase):

    @patch("form_marketing.middleware.BusinessView")
    def test_call(self, MockBusinessView):
        # setup
        get_response = Mock(return_value="response")
        request = Mock()

        response = ViewTrackingMiddleware(get_response)(request)

        # asserts
        MockBusinessView.create_from_request.assert_called_once_with(request)
        get_response.assert_called_once_with(request)
        self.assertEqual(response, "response")
