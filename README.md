#HangPanels [![docs](https://readthedocs.org/projects/hangpanels/badge/?version=latest)](http://hangpanels.readthedocs.org/en/latest/)

Easily explore your Hangouts conversations using Pandas.

```bash
pip install hangpanels
conda install hangpanels
```

## Docs

Check the documentation [here](http://hangpanels.readthedocs.org/en/latest/).


## How to

Get your own Google Hangouts archive from [https://takeout.google.com/settings/takeout](https://takeout.google.com/settings/takeout).
Download the Hangouts archives, and pass the file reference as argument for the ChatsPanel() object.

```python
from hangpanels import ChatsPanel

chats = ChatsPanel("Hangouts.json")
```

## License
MIT Check LICENSE.md
