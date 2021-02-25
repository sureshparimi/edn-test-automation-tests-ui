import json


class Locators:

    def __init__(self, file_path: str, delimiter: str = ">"):
        with open(file_path) as json_file:
            self.__json_data: dict = json.load(json_file)
        self.__delimiter = delimiter
        self.__locale: str = None
        

    def set_locale(self, locale: str):
        self.__locale = locale

    def get_locale(self) -> str:
        return self.__locale

    def parse_and_get(self, json_locator_path: str) -> str:
        json_keys = [key.strip() for key in json_locator_path.split(self.__delimiter)]
        print("I am in parser and get method" + str(json_keys))
        return self.get(*json_keys)

    def get(self, *args) -> str:
        result = self.__json_data

        for arg in args:
            # if anywhere in the hierarchy, we have diff data for diff locales, get the locale specific data
            if self.__locale and self.__locale in result:
                result = result[self.__locale]
            # keep going down the hierarchy and fetch
            result = result[arg]

        # if the field we're fetching has locale specific data
        if self.__locale and self.__locale in result:
            result = result[self.__locale]

        return result
