import re
import patterns


class UObject(object):
    """
    This is the main urljects object, it is able to join strings and
    regular expressions. The value of this object will always be regular
    expression usable in django url.
    """

    def __init__(self, value=patterns.beginning, separator=patterns.SEPARATOR):
        self.value = value
        self.separator = separator

    def add_part(self, part):
        """
        Function for adding partial pattern to the value
        :param part: string or compiled pattern
        """

        if isinstance(part, re._pattern_type):
            part = part.pattern

        if self.value == patterns.beginning:
            self.value += part
        else:
            self.value += self.separator + part
        return self

    def __div__(self, other):
        self.add_part(other)
        return self

    def __repr__(self):
        return self.value

U = UObject()
