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

    def test_row_value(self):
        df = self.panel[self.panel.axes[0][1]]
        self.assertListEqual(list(df.values[0]), ['Hola uno dos, esto es un test',
                                                  '8B2mCoglzQl8B2mEQn_iVb',
                                                  '113614622467621114426'])
