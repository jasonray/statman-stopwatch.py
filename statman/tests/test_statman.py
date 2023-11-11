import unittest
import time
from statman import Statman
import pytest


class TestStatman(unittest.TestCase):
    _accepted_variance = 0.1

    @pytest.fixture(autouse=True)
    def run_before_and_after_tests(data):
        print('reset registry between tests')
        Statman.reset()

    def test_create_stopwatch_directly(self):
        from statman import Stopwatch
        sw = Stopwatch()
        sw.start()
        time.sleep(1)
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)

    def test_create_stopwatch_via_statman_package(self):
        import statman
        sw = statman.Stopwatch()
        sw.start()
        time.sleep(1)
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)

    def test_create_stopwatch_via_statman_constructor(self):
        sw = Statman.stopwatch()
        sw.start()
        time.sleep(1)
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)

    def test_create_stopwatch_via_statman_constructor_autostart(self):
        sw = Statman.stopwatch(autostart=True)
        time.sleep(1)
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)

        sw = Statman.stopwatch(autostart=False)
        time.sleep(1)
        self.assertIsNone(sw.read())

    def test_access_stopwatch_through_registry_get(self):
        Statman.stopwatch('stopwatch-name').start()
        time.sleep(1)

        sw = Statman.get('stopwatch-name')
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)

    def test_access_stopwatch_through_registry_stopwatch(self):
        Statman.stopwatch('stopwatch-name').start()
        time.sleep(1)

        sw = Statman.stopwatch('stopwatch-name')
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)

    def test_ensure_reset_between_tests(self):
        sw = Statman.get('stopwatch-name')
        self.assertIsNone(sw)

    def test_registry_count_0(self):
        self.assertEqual(0, Statman.count())

    def test_registry_count_1(self):
        Statman.stopwatch('stopwatch-name')
        self.assertEqual(1, Statman.count())

    def test_registry_count_2(self):
        Statman.stopwatch('stopwatch-name')
        Statman.stopwatch('stopwatch-name2')
        self.assertEqual(2, Statman.count())

    def test_registry_count_duplicates(self):
        Statman.stopwatch('stopwatch-name')
        Statman.stopwatch('stopwatch-name')
        Statman.stopwatch('stopwatch-name2')
        self.assertEqual(2, Statman.count())

    def test_registry_count_with_reset(self):
        Statman.stopwatch('stopwatch-name')
        Statman.reset()
        Statman.stopwatch('stopwatch-name2')
        self.assertEqual(1, Statman.count())

    def test_dual_stopwatches_read(self):
        Statman.stopwatch(name='a', autostart=False)
        Statman.stopwatch(name='b', autostart=False)

        Statman.stopwatch('a').start()
        time.sleep(0.3)

        Statman.stopwatch('b').start()
        time.sleep(0.3)

        self.assertAlmostEqual(Statman.stopwatch('a').read(), 0.6, delta=self._accepted_variance)
        self.assertAlmostEqual(Statman.stopwatch('b').read(), 0.3, delta=self._accepted_variance)

    def test_dual_stopwatches_read_with_get(self):
        Statman.stopwatch(name='a', autostart=False)
        Statman.stopwatch(name='b', autostart=False)

        Statman.stopwatch('a').start()
        time.sleep(0.3)

        Statman.get('b').start()
        time.sleep(0.3)

        self.assertAlmostEqual(Statman.stopwatch('a').read(), 0.6, delta=self._accepted_variance)
        self.assertAlmostEqual(Statman.get('b').read(), 0.3, delta=self._accepted_variance)

    def test_simplified_access(self):
        from statman import Statman as SM

        SM.stopwatch(name='a', autostart=False)
        SM.stopwatch(name='b', autostart=False)

        SM.stopwatch('a').start()
        time.sleep(0.3)

        SM.get('b').start()
        time.sleep(0.3)

        self.assertAlmostEqual(SM.stopwatch('a').read(), 0.6, delta=self._accepted_variance)
        self.assertAlmostEqual(SM.get('b').read(), 0.3, delta=self._accepted_variance)

    def test_manually_registry(self):
        from statman import Stopwatch
        sw = Stopwatch()
        Statman.register('sw',sw)
        
        Statman.get('sw').start()
        time.sleep(1)
        self.assertAlmostEqual(sw.read(), 1, delta=0.1)