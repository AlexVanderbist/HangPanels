import json
import pandas as pd


class ChatsPanel(pd.Panel):

    def __init__(self, json_log, *args, **kwargs):
        self.path = json_log
        super(ChatsPanel, self).__init__(self.load_json(), *args, **kwargs)

    def load_json(self):
        with open(self.path) as json_data:
            data = json.load(json_data)

        frames = {}
        for conversation in data["conversation_state"]:
            frames[conversation["conversation_state"]["conversation_id"]] = self.get_data_frame(conversation)

        return frames

    @staticmethod
    def get_data_frame(conversation):
        """Extracts a whole conversation

        :param conversation: A whole Hangouts log conversation
        :type conversation: dict

        :returns: A pandas.DataFrame with each message as a row
        :rtype: pandas.DataFrame
        """
        return pd.DataFrame()
