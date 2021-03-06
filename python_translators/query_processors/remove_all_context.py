from python_translators.query_processors.query_processor import QueryProcessor
from python_translators.translation_query import TranslationQuery

import copy


class RemoveAllContext(QueryProcessor):
    def __init__(self):
        super(RemoveAllContext, self).__init__(name='remove_all_context')

    def process_query(self, query: TranslationQuery) -> TranslationQuery:
        new_query = copy.copy(query)

        new_query.before_context = ''
        new_query.after_context = ''

        return new_query
