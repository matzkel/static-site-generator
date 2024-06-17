import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        same_node = TextNode("This is a text node", "bold")
        self.assertEqual(node, same_node)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        diff_node = TextNode("This is a different text node", "normal")
        self.assertNotEqual(node, diff_node)


if __name__ == "__main__":
    unittest.main()