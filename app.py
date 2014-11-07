#!/usr/bin/env python

import os
import sys
import tornado.web
import tornado.httpserver
import tornado.ioloop
from time import time
from uuid import uuid4
from tornado.options import define, options

from crate.client import connect
from crate.client.exceptions import ProgrammingError


define('port', default=8080, help='run on the given port', type=int)

crate_host = os.environ.get('DB_PORT_4200_TCP_ADDR', '127.0.0.1')
crate_port = os.environ.get('DB_PORT_4200_TCP_PORT', '4200')
crate_server = '{}:{}'.format(crate_host, crate_port)


def init_tables():
    conn = connect(crate_server)
    c = conn.cursor()
    try:
        c.execute('create table logs (id string primary key, ts timestamp)')
    except ProgrammingError:
        pass


class Index(tornado.web.RequestHandler):
    def get(self):
        conn = connect(crate_server)
        c = conn.cursor()
        c.execute('insert into logs (id, ts) values (?, ?)',
                  (str(uuid4()), int(time() * 1000)))
        c.execute('select count(*) from logs')
        number = c.fetchone()[0]
        self.write('Hello Number {0}'.format(number))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', Index)]
        settings = {'title': 'Demo', 'debug': True}
        super().__init__(handlers, **settings)


def main():
    init_tables()
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port, '0.0.0.0')
    try:
        message = 'Starting tornado server on http://localhost:{port}'
        print(message.format(port=options.port))
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
