import os
import lso
import unittest
import tempfile

class LSOTestCase(unittest.TestCase):
    def setUp(self):
        """Before each test, create a new database."""
        self.db_file, lso.app.config['DATABASE'] = tempfile.mkstemp()
        lso.app.config['TESTING'] = True
        lso.app.config['CSRF_ENABLED'] = False
        self.app = lso.app.test_client()
        lso.database.init()

    def tearDown(self):
        os.close(self.db_file)
        os.unlink(lso.app.config['DATABASE'])

    def contact(self, data):
        """POST data to the contact form."""
        return self.app.post('/contact', data=data)

    def test_contact_form(self):
        subject = 'subject'
        reply_to = 'a@example.com'
        message_body = 'body'
        sender = lso.app.config['DEFAULT_MAIL_SENDER']

        with lso.mail.record_messages() as outbox:
            # subject, email, and message
            result = self.contact(dict(subject=subject,
                                       email=reply_to,
                                       message=message_body))

            self.assertEqual(len(outbox), 1)
            message = outbox[0]
            self.assertEqual(message.sender, sender)
            self.assertEqual(message.subject, subject)
            self.assertEqual(message.reply_to, reply_to)
            self.assertEqual(message.body, message_body)

            # invalid email
            result = self.contact(dict(subject=subject,
                                       email='aoeu',
                                       message=message_body))

            self.assertEqual(len(outbox), 1)

            # subject and message
            result = self.contact(dict(subject=subject,
                                       message=message_body))

            self.assertEqual(len(outbox), 2)
            message = outbox[1]
            self.assertEqual(message.sender, sender)
            self.assertEqual(message.subject, subject)
            self.assertEqual(message.reply_to, None)
            self.assertEqual(message.body, message_body)

            # just subject
            result = self.contact(dict(subject=subject))
            self.assertEqual(len(outbox), 2)

            # just message
            result = self.contact(dict(message=message_body))
            self.assertEqual(len(outbox), 2)

if __name__ == '__main__':
    unittest.main()
