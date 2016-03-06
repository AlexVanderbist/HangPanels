import json
import pandas
import datetime
from utils import DotDictify
from collections import Counter


class ChatsPanel(pandas.Panel):
    """
    Creates a :py:class:`pandas.Panel` where each :py:class:`pandas.DataFrame` is a conversation from the
    `Hangouts.json` log file indexed by the time of each message. It tries to handle as much attachments as possible.
    Right now supports image and place attachments, adding the url to those objects as the message text.
    """

    def __init__(self, json_log, *args, **kwargs):
        super(self.__class__, self).__init__(self.load_json(json_log), *args, **kwargs)

    def head(self, n=5):
        raise NotImplementedError

    def tail(self, n=5):
        raise NotImplementedError

    def align(self, other, **kwargs):
        raise NotImplementedError

    def _constructor_expanddim(self):
        raise NotImplementedError

    def load_json(self, json_log):
        """
        Loads the JSON file at the instantiation.

        :param json_log: Reference to the log file
        :type json_log: string

        :return: Creates a dictionary of pandas.DataFrame
        :rtype: dict
        """

        with open(json_log) as json_data:
            data = DotDictify(json.load(json_data))

        frames = {}

        for conversation in data.conversation_state:
            df = self.get_data_frame(conversation)
            if isinstance(df, pandas.DataFrame):
                name = conversation.conversation_state.conversation.get("name", False)
                if name:
                    frames[name.title().replace(" ", "_")] = df
                else:
                    users = []

                    for user in conversation.conversation_state.conversation.participant_data:
                        if user.get("fallback_name", False):
                            users.append(user.get("fallback_name"))
                        else:
                            users.append(conversation.conversation_state.conversation_id.id[4:8])

                    frames["_".join(u.title().replace(" ", "_") for u in users)] = df

        return frames

    @staticmethod
    def get_data_frame(conversation):
        """
        Extracts a whole conversation.

        :param conversation: A whole Hangouts log conversation
        :type conversation: utils.DotDictify

        :returns: A pandas.DataFrame with each message as a row
        :rtype: pandas.DataFrame
        """

        event_list = []

        for event in conversation.conversation_state.event:
            event_id = event.get("event_id", False)
            sender_id = event.sender_id.gaia_id
            timestamp = datetime.datetime.fromtimestamp(float(event.timestamp)/1000000)
            text = []

            if event.get("chat_message", False):
                message_content = event.chat_message.message_content

                if message_content.get("segment", False):
                    for segment in message_content.segment:
                        if segment.type.lower() in ["text", "link"] and segment.get("text", False):
                            text.append(segment.text)

                if message_content.get("attachment", False):
                    for attachment in message_content.attachment:
                        if attachment.embed_item.type[0].lower() == "PLUS_PHOTO".lower():
                            text.append(attachment.embed_item["embeds.PlusPhoto.plus_photo"].url)
                        if attachment.embed_item.type[0].lower() == "PLACE_V2".lower():
                            text.append(attachment.embed_item.id)

                event_list.append({"timestamp": timestamp,
                                   "event_id": event_id,
                                   "sender_id": sender_id,
                                   "content": " ".join(text)})

            else:
                continue

        if len(event_list) > 0:
            return pandas.DataFrame(event_list).set_index("timestamp")
        else:
            return None

    def conversations(self):
        """
        See all chats in the panel. The name is taken from the chat if exists, if not, takes the :code:`fallback_name`
        of each user and puts them together.

        :return: Name of the chats
        :rtype: numpy.ndarray
        """
        return self.axes[0].values
