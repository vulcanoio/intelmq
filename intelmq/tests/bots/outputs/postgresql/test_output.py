# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras
import unittest

import intelmq.lib.test as test
from intelmq.bots.outputs.postgresql.output import PostgreSQLOutputBot


INPUT1 = {"__type": "Event",
          "classification.identifier": "zeus",
          "classification.type": "botnet drone",
          "source.asn": 64496,
          "source.ip": "192.0.2.1",
          "feed.name": "Example Feed",
          }


@test.skip_database()
class TestPostgreSQLOutputBot(test.BotTestCase, unittest.TestCase):

    @classmethod
    def set_bot(cls):
        cls.bot_reference = PostgreSQLOutputBot
        cls.default_input_message = INPUT1
        cls.sysconfig = {"host": "localhost",
                         "port": 5432,
                         "database": "intelmq",
                         "user": "intelmq",
                         "password": "intelmq",
                         "sslmode": "require",
                         "table": "tests",}
        cls.con = psycopg2.connect(database=cls.sysconfig['database'],
                                   user=cls.sysconfig['user'],
                                   password=cls.sysconfig['password'],
                                   host=cls.sysconfig['host'],
                                   port=cls.sysconfig['port'],
                                   sslmode=cls.sysconfig['sslmode'],
                                   )
        cls.con.autocommit = True
        cls.cur = cls.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def test_event(self):
        self.run_bot()
        self.cur.execute('SELECT "classification.identifier", "classification.type", "source.asn",'
                         ' "source.ip", "feed.name" FROM tests')
        self.assertEqual(self.cur.rowcount, 1)
        del INPUT1['__type']
        from_db = {k: v for k, v in self.cur.fetchone().items() if v is not None}
        self.assertDictEqual(from_db, INPUT1)

    @classmethod
    def tearDownClass(cls):
        cls.cur.execute('TRUNCATE "tests"')
        cls.cur.close()
        cls.con.close()


if __name__ == '__main__':
    unittest.main()
