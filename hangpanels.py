import json
import pandas
import datetime


class ChatsPanel(pandas.Panel):
    """
    Creates a pandas.Panel where each pandas.DataFrame is a conversation from the `Hangouts.json` log file
    indexed by the time of each message. It tries to handle as much attachments as possible.
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
        Loads the JSON file

        :param json_log: Reference to the log file
        :type json_log: string

        :return: Creates a dictionary of pandas.DataFrame
        :rtype: dict
        """

        with open(json_log) as json_data:
            data = json.load(json_data)

        frames = {}
        for conversation in data["conversation_state"]:
            df = self.get_data_frame(conversation)
            if isinstance(df, pandas.DataFrame):
                frames[conversation["conversation_state"]["conversation_id"]["id"]] = df

        return frames

    @staticmethod
    def get_data_frame(conversation):
        """
        Extracts a whole conversation

        :param conversation: A whole Hangouts log conversation
        :type conversation: dict

        :returns: A pandas.DataFrame with each message as a row
        :rtype: pandas.DataFrame
        """

        try:
            event_list = []

            for event in conversation["conversation_state"]["event"]:
                event_id = event["event_id"]
                sender_id = event["sender_id"]
                timestamp = datetime.datetime.fromtimestamp(float(event["timestamp"])/1000000)
                text = list()

                try:
                    message_content = event["chat_message"]["message_content"]

                    try:
                        for segment in message_content["segment"]:
                            if segment["type"].lower() in ["text", "link"]:
                                text.append(segment["text"])

                    except KeyError:
                        # may happen when there is no (compatible) attachment
                        pass

                    try:
                        for attachment in message_content["attachment"]:
                            # if there is a Google+ photo attachment we append the URL
                            if attachment["embed_item"]["type"][0].lower() == "PLUS_PHOTO".lower():
                                text.append(attachment["embed_item"]["embeds.PlusPhoto.plus_photo"]["url"])

                    except KeyError:
                        pass

                except KeyError:
                    continue

                event_list.append({"timestamp": timestamp,
                                   "event_id": event_id,
                                   "sender_id": sender_id["gaia_id"],
                                   "content": " ".join(text)})
            if len(event_list) > 0:
                return pandas.DataFrame(event_list).set_index('timestamp')
            else:
                return None

        except KeyError:
            raise RuntimeError(
                "The conversation with id: {} could not be extracted.".format(conversation["conversation_id"]["id"]))
