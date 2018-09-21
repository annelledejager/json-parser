import logging

logging.basicConfig(format='%(message)s')


class JsonParser(object):
    """
    Parses an input json array to a nested dictionary of dictionaries of arrays, with keys specified arguments and the
    leaf values as arrays of flat dictionaries matching appropriate groups.
    """

    def __init__(self, args, json_input):
        self.args = args
        self.json_input = json_input

    @staticmethod
    def _create_nested_dictionary(dictionary, keys, leaf_values):
        """
        Create nested dictionary from keys with leaf values
        """
        for key in keys[:-1]:
            dictionary = dictionary.setdefault(key, {})
        dictionary[keys[-1]] = [leaf_values]

    def _strip_nesting_keys(self, group):
        """
        Strip nesting keys out from the dictionaries in the leaves
        """
        for index in range(len(self.args)):
            del group[self.args[index]]

    def _get_group_keys(self, group):
        try:
            return [group[arg] for arg in self.args]
        except KeyError:
            error_message = 'Key does not exist in json input'
            logging.error(error_message)
            raise Exception(error_message)

    def parse(self):
        """
        Parse input json
        """
        parsed_json_result = []
        if not self.args:
            return self.json_input

        try:
            for group in self.json_input:
                group_keys = self._get_group_keys(group)
                self._strip_nesting_keys(group)

                nested_group = {}
                self._create_nested_dictionary(nested_group, group_keys, group)
                parsed_json_result.append(nested_group)
        except TypeError:
            error_message = 'Incorrect input type'
            logging.error(error_message)
            raise Exception(error_message)

        return parsed_json_result
