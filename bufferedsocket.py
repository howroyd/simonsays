#!./.venv/bin/python3
import collections
import dataclasses
import socket


@dataclasses.dataclass(slots=True)
class Buffer:
    '''Buffer for reading from a socket'''
    buffer: collections.deque[bytes] = dataclasses.field(default_factory=collections.deque)
    delimiter: bytes = b'\r\n'

    def _pop_until_delimiter(self) -> bytes | None:
        '''Pops data from the buffer until the delimiter is found'''
        data: bytes | None = None

        try:
            data = self.buffer.popleft()
            while b'\r\n' not in data:
                data += self.buffer.popleft()
        except IndexError:
            if data:
                #  Didn't find the delimiter, but there's still data in the buffer
                self.buffer.appendleft(data)
            return None

        line, rest = data.split(b'\r\n', maxsplit=1)
        if rest:
            self.buffer.appendleft(rest)

        return line

    def read(self) -> bytes:
        '''Reads a line from the buffer'''
        return self._pop_until_delimiter()

    def readlines(self) -> list[bytes]:
        '''Reads all lines from the buffer'''
        lines: list[bytes] = []

        while True:
            line = self.read()
            if not line:
                break
            lines.append(line)

        return lines

    def write(self, data: bytes) -> None:
        '''Writes a chunk of data to the buffer'''
        self.buffer.append(data)

    def __len__(self) -> int:
        '''Returns the number of chunks in the buffer'''
        return len(self.buffer)


@dataclasses.dataclass(slots=True)
class BufferedSocket:
    '''Buffered socket'''
    sock: socket.socket
    buffer: Buffer = dataclasses.field(default_factory=Buffer)

    def close(self) -> None:
        '''Closes the socket'''
        self.sock.close()

    def read(self) -> bytes | None:
        '''Reads a line from the socket'''
        try:
            data = self.sock.recv(4096)
            self.buffer.write(data)
        except socket.timeout:
            pass
        return self.buffer.read()

    def readlines(self) -> list[bytes]:
        '''Reads all lines from the socket'''
        try:
            data = self.sock.recv(4096)
            self.buffer.write(data)
        except socket.timeout:
            pass
        return self.buffer.readlines()

    def write(self, data: bytes) -> None:
        '''Writes a chunk of data to the socket'''
        self.sock.sendall(data)

    def __len__(self) -> int:
        '''Returns the number of chunks in the buffer'''
        return len(self.buffer)


def create_connection(dest: tuple[str, int], timeout: float = 0.1) -> BufferedSocket:
    '''Creates a socket connection to the specified destination'''
    return BufferedSocket(socket.create_connection(dest, timeout=timeout))
