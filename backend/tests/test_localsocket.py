import asyncio
import unittest

from decky_loader.localplatform.localsocket import UnixSocket


class TestSocket(UnixSocket):
    async def read_single_line_from(self, reader: asyncio.StreamReader) -> str | None:
        return await self._read_single_line(reader)


class ReadSingleLineTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_none_at_eof(self) -> None:
        reader = asyncio.StreamReader()
        reader.feed_eof()

        socket = TestSocket()

        self.assertIsNone(await socket.read_single_line_from(reader))

    async def test_discards_incomplete_message_at_eof(self) -> None:
        reader = asyncio.StreamReader()
        reader.feed_data(b'{"incomplete": true}')
        reader.feed_eof()

        socket = TestSocket()

        self.assertIsNone(await socket.read_single_line_from(reader))

    async def test_empty_line_is_not_eof(self) -> None:
        reader = asyncio.StreamReader()
        reader.feed_data(b"\n")
        reader.feed_eof()

        socket = TestSocket()

        self.assertEqual(await socket.read_single_line_from(reader), "\n")


if __name__ == "__main__":
    unittest.main()
