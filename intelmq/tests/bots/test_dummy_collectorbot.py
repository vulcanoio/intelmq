# -*- coding: utf-8 -*-
"""


Test with reports
"""
import unittest

import intelmq.lib.bot as bot
import intelmq.lib.test as test
from intelmq.lib.message import Report

EXAMPLE_REPORT = {"__type": "Report",
                  "feed.name": "Example Feed",
                  "feed.code": "Example Code",
                  "feed.accuracy": 100.0,
                  'raw': 'dGVzdA=='
                  }


class DummyCollectorBot(bot.CollectorBot):
    """
    A dummy collector bot only for testing purpose.
    """

    def process(self):
        report = Report()
        if self.parameters.raw:
            report['raw'] = 'test'
        self.send_message(report)

    def recover_line(self, line):
        return '\n'.join([self.tempdata[0], line, self.tempdata[1]])


class TestDummyCollectorBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for a DummyBot.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = DummyCollectorBot
        cls.default_input_message = None
        cls.sysconfig = {'feed': 'Example Feed',
                         'code': 'Example Code',
                         'raw': True
                         }

    def test_event(self):
        """ Test if correct Event has been produced. """
        self.run_bot()
        self.assertMessageEqual(0, EXAMPLE_REPORT)

    def test_missing_raw(self):
        """ Test if correct Event has been produced. """
        self.sysconfig['raw'] = False
        self.run_bot()
        self.assertAnyLoglineEqual(message='Ignoring report without raw field. '
                                           'Possible bug or misconfiguration of this bot.',
                                   levelname='WARNING')


if __name__ == '__main__':
    unittest.main()
