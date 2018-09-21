import unittest
import pycodestyle


class TestPep8(unittest.TestCase):
    defaults = {
        'ignore': ['E501'],
        'repeat': True,
    }

    def test_pep8(self):
        kwargs = self.defaults.copy()
        style = pycodestyle.StyleGuide(**kwargs)
        report = style.check_files(paths=['/app/'])
        self.assertEqual(report.total_errors, 0, msg=report)
