from needle.diff import ImageDiff
from needle.driver import NeedleWebDriver
import os
from PIL import Image
import sys
import unittest2

def _object_filename(obj):
    return os.path.abspath(sys.modules[type(obj).__module__].__file__)

class NeedleTestCase(unittest2.TestCase):
    driver_command_executor = 'http://127.0.0.1:4444/wd/hub'
    driver_desired_capabilities = {
        'browserName': 'firefox',
    }
    driver_browser_profile = None

    capture = False

    def __call__(self, *args, **kwargs):
        self.driver = self.get_web_driver()
        super(NeedleTestCase, self).__call__(*args, **kwargs)
        self.driver.close()
    
    def get_web_driver(self):
        return NeedleWebDriver(
            self.driver_command_executor,
            self.driver_desired_capabilities,
            self.driver_browser_profile
        )

    def assertScreenshot(self, element, name, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.

        A name is required for the screenshot, which will be appended with ``.png``.
        """
        if isinstance(name, basestring):
            filename = os.path.join(
                os.path.dirname(_object_filename(self)),
                '%s.png' % name
            )
        else:
            # names can be filehandles for testing. This sucks - we
            # should write out files to their correct location
            filename = name
        if self.capture:
            if os.path.exists(filename):
                self.skipTest('Not capturing %s, image already exists. If you '
                              'want to capture this element again, delete %s'
                              % (name, filename))
            element.get_screenshot().save(filename)
        else:
            image = Image.open(filename)
            diff = ImageDiff(element.get_screenshot(), image)
            self.assertAlmostEqual(diff.get_distance(), 0, delta=threshold)


    

