#!/usr/bin/env python3

import sys

def encode_u32(num):
    if num >= 2 ** 32:
        raise TypeError("num must be a u32")
    to_return = [(num >> (8 * x))&0xFF for x in range(4)]
    to_return.reverse()
    return bytes(to_return)

class Streamer:
    def __init__(self, out):
        self.out = out

    def start_file(self, filename):
        if not filename:
            raise TypeError("Bad filename")
        self.write_chunk(filename.encode())

    def _write_u32(self, num):
        self.out.write(encode_u32(num))

    def write_chunk(self, buf):
        if buf:
            bytes_buf = bytes(buf)
            buf_size = len(bytes_buf)
            self._write_u32(buf_size)
            self.out.write(bytes_buf)

    def write_from(self, reader):
        chunk = True
        while chunk:
            chunk = i.read(BUF_SIZE)
            out.write_chunk(chunk)

    def end_file(self):
        self._write_u32(0)

    def close(self):
        self.out.close()

    def __exit__(self, type, value, traceback):
        self.close()

    def __enter__(self):
        return self

BUF_SIZE=2**12
with Streamer(sys.stdout.buffer) as out:
    for filename in sys.argv[1:]:
        out.start_file(filename)
        with open(filename, "rb") as i:
            out.write_from(i)
        out.end_file()
