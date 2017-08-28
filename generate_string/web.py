# coding: utf-8

import asyncio

import os
import websockets

from generate_string.generators import random_value

STATIC_PATH = 'templates'
HOST = '127.0.0.1'
UPDATE_INTERVAL = 1


async def websocket_handler(web_socket, path):
    print('Connected to %s' % web_socket.host + path)
    while True:
        await web_socket.send(random_value())
        await asyncio.sleep(UPDATE_INTERVAL)


def with_head(fn):
    def inner(*args, **kwargs):
        head = b'HTTP/1.1 200 OK\r\n'
        head += b'Content-Type: text/html\r\n'
        head += b'\r\n'
        return head + fn(*args, **kwargs)
    return inner


class Service(asyncio.Protocol):

    @with_head
    def render(self, template_name):
        head = b'HTTP/1.1 200 OK\r\n'
        head += b'Content-Type: text/html\r\n'
        head += b'\r\n'

        with open(os.path.join(STATIC_PATH, template_name), 'rb') as fh:
            html = fh.read()
        return html

    def connection_made(self, tr):
        self.tr = tr
        self.total = 0

    def data_received(self, data):
        if data:
            resp = self.render('index.html')
            self.tr.write(resp)
        self.tr.close()


async def start_web_server():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(Service, HOST, 8080)
    await server.wait_closed()


async def start_socket_server():
    await websockets.serve(websocket_handler, HOST, 8081)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    loop.create_task(start_socket_server())
    try:
        loop.run_forever()
    except Exception:
        loop.close()


if __name__ == '__main__':
    main()
