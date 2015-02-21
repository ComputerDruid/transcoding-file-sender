#!/usr/bin/env python3

import sys
import struct

class NoMoreFilesError(Exception):
    pass

class StreamingReader:
    BLOCK_SIZE = 2**12
    def __init__(self, buf):
        self.buf = buf

    def read_exactly(self, num):
        b = [0]*num
        num_read = 0
        num_to_read = num
        while num_read < num:
            bytes_read = self.buf.read(num_to_read)
            if len(bytes_read) == 0:
                raise IOError("Unexpected EOF")
            num_to_read -= len(bytes_read)
            b[num_read:num_read+len(bytes_read)] = bytes_read
            num_read += len(bytes_read)
        return bytes(b)

    def read_u32(self):
        u32_bytes = self.read_exactly(4)
        return struct.unpack(">I", u32_bytes)[0]

    def read_filename(self):
        filename_size = self.read_u32()
        filename_bytes = self.read_exactly(filename_size)
        return filename_bytes.decode('utf-8')

    def read_file(self):
        try:
            filename = self.read_filename()
        except IOError:
            raise NoMoreFilesError("No more files left in the stream")

        bytes_left = self.read_u32()
        with open(filename, "wb") as out:
            while bytes_left > 0:
                while bytes_left > 0:
                    buf = self.buf.read1(min(self.BLOCK_SIZE, bytes_left))
                    bytes_left -= len(buf)
                    out.write(buf)
                bytes_left = self.read_u32()

    def read_files(self):
        try:
            while True:
                self.read_file()
        except NoMoreFilesError:
            pass

i = StreamingReader(sys.stdin.buffer)
print(i.read_files())
