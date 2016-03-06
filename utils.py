class DotDictify(dict):
    """
    Get's a :py:class:`dict` and creates a dot searchable dictionary. Key errors when navigating in a dictionary
    are managed much more easily.

    :return: A new instance
    :rtype: utils.DotDictify
    """

    __getattr__ = dict.__getitem__

    def __init__(self, d):
        self.update(**dict((k, self.parse(v))
                           for k, v in d.items()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v
