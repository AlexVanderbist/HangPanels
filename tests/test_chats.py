import unittest
from hangpanels import ChatsPanel


class TestChatsPanel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.panel = ChatsPanel("Hangouts.json")

    def test_instance(self):
        self.assertIsInstance(self.panel, ChatsPanel)

    def test_number_of_chats(self):
        self.assertEqual(self.panel.shape, (2, 20, 3))
