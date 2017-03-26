# -*- coding: utf-8 -*-

import os
import re

from googleapiclient.discovery import build
from configobj import ConfigObj

from context_aware_translator import ContextAwareTranslator

CONFIG_FILE_PATH = '~/.config/translators.cfg'


class GoogleTranslator(ContextAwareTranslator):

    def __init__(self, key=None):

        if not key:
            try:
                config_file = os.path.expanduser(CONFIG_FILE_PATH)
                config = ConfigObj(config_file)
                key = config['TRANSLATE_API_KEY']
            except KeyError:
                raise Exception('No config file found. Create config file or pass key as argument to constructor')

        self.key = key
        self.translation_service = build('translate', 'v2', developerKey=key)

    # This translation is not aware of context
    def translate(self, query, source_language, target_language):
        """
        Translate a query from source language to target language
        :param query:
        :param source_language:
        :param target_language:
        :return:
        """

        params = {
            'source': source_language,
            'target': target_language,
            'q': query,
            'format': 'html'
        }

        translations = self.translation_service.translations().list(**params).execute()

        return translations['translations'][0][u'translatedText']

    def ca_translate(self, query, source_language, target_language, before_context ='', after_context=''):
        """
        Function to translate a query by taking into account the context
        :param query:
        :param source_language:
        :param target_language:
        :param before_context:
        :param after_context:
        :return:
        """
        query = before_context + '<span>' + query + '</span>' + after_context

        translation = self.translate(query, source_language, target_language)
        translated_query = GoogleTranslator.parse_spanned_string(translation)

        return translated_query

    @staticmethod
    def parse_spanned_string(spanned_string):
        re_opening_tag = re.compile(r"<[\s]*[sS]pan[\s]*>(.*)", flags=re.DOTALL)  # <span> tag

        search_obj = re_opening_tag.search(spanned_string)
        if not search_obj:
            raise Exception('Failed to parse spanned string: no opening span tag found.')

        trail = search_obj.group(1)

        re_closing_tag = re.compile(r"(.*)<[\s]*/[\s]*[sS]pan[\s]*>", flags=re.DOTALL)  # </span> tag

        search_obj = re_closing_tag.search(trail)

        if not search_obj:
            raise Exception('Failed to parse spanned string: no closing tag found.')

        result = search_obj.group(1)

        return result.strip()


if __name__ == '__main__':
    translator = GoogleTranslator('AIzaSyC6hioSx_nb1HCmt719hLK-HS6OHG0D7-8')

    print(translator.ca_translate(query=u'klein', before_context=u'Ein', after_context=u'jägermeister', source_language='es', target_language='en'))
