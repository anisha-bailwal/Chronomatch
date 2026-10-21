
import unittest
from src.ipc.ring_buffer import RingBuffer


class TestRingBuffer(unittest.TestCase):

    def setUp(self):
        self.buffer = RingBuffer(capacity=3)

    def tearDown(self):
        self.buffer.close()

    def test_read_empty_buffer(self):
        self.assertIsNone(self.buffer.read())

    def test_write_and_read_order(self):
        self.assertTrue(self.buffer.write(101, 250.50, 10))
        self.assertEqual(
            self.buffer.read(),
            (101, 250.50, 10)
        )

    def test_full_buffer_rejects_order(self):
        self.buffer.write(101, 250.50, 10)
        self.buffer.write(102, 251.00, 5)
        self.buffer.write(103, 249.75, 8)

        self.assertFalse(
            self.buffer.write(104, 252.00, 2)
        )

    def test_wrap_around(self):
        self.buffer.write(101, 250.50, 10)
        self.buffer.write(102, 251.00, 5)
        self.buffer.write(103, 249.75, 8)

        self.buffer.read()
        self.buffer.read()

        self.assertTrue(
            self.buffer.write(104, 252.00, 2)
        )
        self.assertTrue(
            self.buffer.write(105, 253.00, 4)
        )

        self.assertEqual(
            self.buffer.read(), (103, 249.75, 8)
        )
        self.assertEqual(
            self.buffer.read(), (104, 252.00, 2)
        )
        self.assertEqual(
            self.buffer.read(), (105, 253.00, 4)
        )

    def test_invalid_capacity_is_rejected(self):
        for capacity in (0, -1, True, 1.5):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    RingBuffer(capacity)

    def test_size_of_empty_buffer(self):
            self.assertEqual(self.buffer.size(), 0)

    def test_available_space_initially(self):
        self.assertEqual(self.buffer.available_space(), 3)

    def test_is_empty_and_is_full(self):
        self.assertTrue(self.buffer.is_empty())
        self.assertFalse(self.buffer.is_full())

        self.buffer.write(101, 250.50, 10)
        self.buffer.write(102, 251.00, 5)
        self.buffer.write(103, 249.75, 8)

        self.assertTrue(self.buffer.is_full())
        self.assertFalse(self.buffer.is_empty())

    def test_size_and_available_space_after_write(self):
        self.buffer.write(101, 250.50, 10)

        self.assertEqual(self.buffer.size(), 1)
        self.assertEqual(self.buffer.available_space(), 2)

        self.buffer.read()

        self.assertEqual(self.buffer.size(), 0)
        self.assertEqual(self.buffer.available_space(), 3)

if __name__ == "__main__":
    unittest.main()

