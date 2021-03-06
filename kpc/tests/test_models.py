from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from model_mommy import mommy

from kpc.models import Certificate, Licensee


class LicenseeTests(SimpleTestCase):

    def setUp(self):
        self.licensee = mommy.prepare(Licensee)

    def test_licensee_returns_name_str(self):
        """String representation of name is model's name value"""
        self.assertEqual(str(self.licensee), self.licensee.name)

    def test_bad_tin_rejection(self):
        """Reject bad tax identifiers"""
        with self.assertRaises(ValidationError):
            self.licensee.tax_id = 'NOT A TIN'
            self.licensee.clean_fields()

    def test_valid_tin_acceptance(self):
        """Properly formatted tax identifiers do not raise ValidationErrors"""
        self.licensee.tax_id = '12-1234567'
        self.licensee.clean_fields()


class CertificateTests(TestCase):

    def setUp(self):
        self.cert = mommy.make(Certificate, number=1)

    def test_display_name(self):
        """Certificates displays as 'US{number}"""
        self.assertEqual(str(self.cert), f'US{self.cert.number}')

    def test_bad_aes_rejection(self):
        """Reject malformed AES identifiers"""
        with self.assertRaises(ValidationError):
            self.cert.aes = 'X15152'
            self.cert.clean_fields()

    def test_accept_valid_aes_rejection(self):
        """Accept valid AES identifiers
            regex: X\d{14}
        """
        self.cert.aes = 'X12345678901234'
        self.cert.clean_fields()

    def test_next_available_when_no_certs(self):
        """Next available cert number is 1 if no certs exist"""
        self.cert.delete()
        self.assertEquals(Certificate.next_available_number(), 1)

    def test_next_available_when_certs(self):
        """Next available cert number is highest existing+1"""
        self.assertEquals(Certificate.next_available_number(), 2)

    def test_default_search_filters_returns_query_params(self):
        """Query parameters for default cert search are generated"""
        expected = 'status=0&status=1&status=2'
        self.assertEqual(Certificate.default_search_filters(), expected)
