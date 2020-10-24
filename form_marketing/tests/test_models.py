from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from model_bakery import baker

from ..models import Campaign, Business, BusinessView, ViewPath


TEST_INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # local
    'home',

    # third party
    'bootstrapform',
]


class CampaignModelTest(TestCase):

    def test_str(self):
        # setup
        c = baker.make(Campaign, name="Test Campaign", view="it:test")

        # asserts
        self.assertEqual(c.__str__(), "Test Campaign at it:test")

    @override_settings(INSTALLED_APPS=TEST_INSTALLED_APPS)
    def test_get_view_choices(self):
        # asserts
        self.assertEqual(
            Campaign.get_view_choices(),
            [["home:landing","landing view in home app"]]
        )

    @patch("form_marketing.models.reverse", return_value="path")
    def test_get_path(self, mock_reverse):
        # setup
        c = baker.make(Campaign, view="it:test")
        path = c.get_path()

        # asserts
        mock_reverse.assert_called_once_with("it:test")
        self.assertEqual(path, "path")


class BusinessTest(TestCase):

    def test_str(self):
        # setup
        b = baker.make(
            Business, name="Test Name",
            campaign__name="Test Campaign",
            campaign__view="landing:home"
        )

        # asserts
        self.assertEqual(b.__str__(), "Test Name on Test Campaign campaign")

    def test_get_from_session_if_key_try(self):
        # setup
        b = baker.make(Business)
        session = {"business_key": b.key}

        # asserts
        self.assertEqual(b, Business.get_from_session(session))

    def test_get_from_session_if_key_except(self):
        # setup
        session = {"business_key": "124"}

        # asserts
        self.assertIsNone(Business.get_from_session(session))

    def test_get_from_session_if_not_key(self):
        # setup
        session = {}

        # asserts
        self.assertIsNone(Business.get_from_session(session))

    def test_get_path(self):
        # setup
        c = baker.make(Campaign, slug="test-slug")
        b = baker.make(Business, key="3dfy", campaign=c)

        # asserts
        self.assertEqual(b.get_path(), "/test-slug/3dfy/")

    def test_save_if_not(self):
        # setup
        b = baker.make(Business, name="Test")

        # asserts
        self.assertIsNotNone(b.key)

    def test_save_if(self):
        # setup
        key = Business.get_new_key()
        b = baker.make(Business, key=key, name="Test")

        # asserts
        self.assertEqual(b.key, key)


class BusinessViewTest(TestCase):

    def test_str(self):
        # setup
        bv = baker.make(
            BusinessView,
            path__path="/",
            business__name="Test Name"
        )

        # asserts
        self.assertEqual(bv.__str__(), "Test Name viewed home:landing")

    def test_create_from_request(self):
        # setup
        b = baker.make(Business)
        p = baker.make(ViewPath)

        request = Mock()
        request.session = {"business_key": b.key}
        request.path = p.path

        bv = BusinessView.create_from_request(request)

        # asserts
        self.assertEqual(bv.path, p)
        self.assertEqual(bv.business, b)


class ViewPathTest(TestCase):

    def test_str(self):
        # setup
        vp = baker.make(ViewPath, path="path")

        # asserts
        self.assertEqual(vp.__str__(), "path")

    def test_get_create_from_request_create(self):
        # setup
        vp = ViewPath.get_create_from_request(Mock(path="path"))

        # asserts
        self.assertEqual(vp.path, "path")

    def test_get_create_from_request_get(self):
        # setup
        vp_1 = baker.make(ViewPath, path="path")
        vp_2 = ViewPath.get_create_from_request(Mock(path="path"))

        # asserts
        self.assertEqual(vp_1, vp_2)

    def test_name(self):
        # setup
        vp = baker.make(ViewPath, path="/")

        # asserts
        self.assertEqual(vp.name, "home:landing")
