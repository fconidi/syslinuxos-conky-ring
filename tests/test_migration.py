from pathlib import Path
import subprocess
import os
from unittest.mock import patch
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SettingsMigrationTests(unittest.TestCase):
    def run_script(self, name, root, *arguments):
        text = (ROOT / 'packaging' / name).read_text()
        text = text.replace('/usr/share/conky/syslinuxos-ring', str(root / 'theme'))
        text = text.replace('/opt/Sys-ring-conky', str(root / 'legacy-theme'))
        text = text.replace('/var/lib/syslinuxos-conky-ring', str(root / 'state'))
        script = root / name
        script.write_text(text)
        subprocess.run(['sh', str(script), *arguments], check=True)

    def test_custom_settings_survive_the_empty_transitional_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'theme').mkdir()
            (root / 'legacy-theme').mkdir()
            settings = root / 'legacy-theme/settings.lua'
            custom = 'THEME = "violet dark"\ncpu_cores = 12\n'
            settings.write_text(custom)
            self.run_script('preinst', root, 'upgrade', '0.1.12')
            settings.unlink()
            settings = root / 'theme/settings.lua'
            settings.write_text('THEME = "blue dark"\n')
            self.run_script('restore-settings.sh', root)
            self.assertEqual(settings.read_text(), custom)
            self.assertFalse((root / 'state/legacy-settings.lua').exists())

    def test_retry_does_not_replace_the_original_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'theme').mkdir()
            (root / 'legacy-theme').mkdir()
            settings = root / 'legacy-theme/settings.lua'
            settings.write_text('original')
            self.run_script('preinst', root, 'install')
            settings.write_text('replacement')
            self.run_script('preinst', root, 'upgrade', '0.1.12')
            settings = root / 'theme/settings.lua'
            settings.write_text('package default')
            self.run_script('restore-settings.sh', root)
            self.assertEqual(settings.read_text(), 'original')

    def test_settings_survive_upgrade_from_standard_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'theme').mkdir()
            settings = root / 'theme/settings.lua'
            settings.write_text('THEME = "violet dark"\n')
            self.run_script('preinst', root, 'upgrade', '0.2.10')
            settings.write_text('THEME = "blue dark"\n')
            self.run_script('restore-settings.sh', root)
            self.assertEqual(settings.read_text(), 'THEME = "violet dark"\n')

    def test_transitional_install_after_new_package_has_no_stale_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'theme').mkdir()
            (root / 'theme/settings.lua').write_text('current settings')
            (root / 'bin').mkdir()
            query = root / 'bin/dpkg-query'
            query.write_text("#!/bin/sh\nprintf 'install ok installed'\n")
            query.chmod(0o755)
            with patch.dict(os.environ, {'DPKG_MAINTSCRIPT_PACKAGE': 'syslinuxos-ring-conky',
                                        'PATH': str(query.parent) + os.pathsep + os.environ['PATH']}):
                self.run_script('preinst', root, 'upgrade', '0.1.12')
            self.assertFalse((root / 'state').exists())

    def test_fresh_install_has_no_legacy_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.run_script('preinst', root, 'install')
            self.run_script('restore-settings.sh', root)
            self.assertFalse((root / 'state').exists())


if __name__ == '__main__':
    unittest.main()
