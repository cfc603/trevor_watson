from django.test import TestCase

from ..templatetags.blog_tags import text_primary


class TextPrimaryTest(TestCase):

    def test_expected_output(self):
        # asserts
        self.assertEqual(
            text_primary("Test Output"),
            "Test <span class='text-primary'>Output</span>"
        )
