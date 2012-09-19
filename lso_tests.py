import os
import lso
import unittest
import tempfile

class LSOTestCase(unittest.TestCase):
    def setUp(self):
        """Before each test, create a new database."""
        self.db_file, lso.app.config['DATABASE'] = tempfile.mkstemp()
        lso.app.config['TESTING'] = True
        self.app = lso.app.test_client()
        lso.database.init()

    def tearDown(self):
        os.close(self.db_file)
        os.unlink(lso.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
