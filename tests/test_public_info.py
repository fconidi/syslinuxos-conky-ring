from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / 'files/usr/share/conky/syslinuxos-ring/public-info.py'
SPEC = spec_from_file_location('ring_public_info', SOURCE)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PublicInfoTests(unittest.TestCase):
    def test_refresh_writes_public_ip_and_isp(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'public-info'
            values = {
                'https://api.ipify.org': '203.0.113.4',
                'https://ipinfo.io/org': 'AS12345 Example ISP\n',
            }
            MODULE.refresh(path, now=1000, fetch=lambda url: values[url])
            self.assertEqual(path.read_text(), '203.0.113.4\nExample ISP\n')

    def test_failed_request_preserves_last_values(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'public-info'
            path.write_text('203.0.113.4\nExample ISP\n')
            MODULE.refresh(path, now=1000, fetch=lambda url: '')
            self.assertEqual(path.read_text(), '203.0.113.4\nExample ISP\n')

    def test_cached_values_avoid_repeat_requests(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'public-info'
            values = {
                'https://api.ipify.org': '203.0.113.4',
                'https://ipinfo.io/org': 'AS12345 Example ISP',
            }
            MODULE.refresh(path, now=1000, fetch=lambda url: values[url])
            MODULE.refresh(path, now=1100, fetch=lambda url: self.fail('unexpected request'))
            self.assertEqual(path.read_text(), '203.0.113.4\nExample ISP\n')

    def test_invalid_values_are_not_displayed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'public-info'
            MODULE.refresh(path, now=1000, fetch=lambda url: 'bad ip' if 'ipify' in url else 'AS3 Evil\nISP${exec}')
            self.assertEqual(path.read_text(), 'N/A\nEvil ISPexec\n')


if __name__ == '__main__':
    unittest.main()
