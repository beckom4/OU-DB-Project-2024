from DB_handler import DB_handler
from TextLoader import TextLoader
from TextBuilder import TextBuilder
from SearchWizard import SearchWizard
from Article import Article

class Database:

    def __init__(self):
        pass
    #     self.db_handler = DB_handler()
    #     self.text_loader = TextLoader()
    #     self.text_builder = TextBuilder()
    #     self.search_wizard = SearchWizard()

    # def add_article(self, article: Article):
    #     reporter_id = self.text_loader.load_reporter(article.authors)
    #     np_id = self.text_loader.load_newspaper(article.newspaper)
    #     article_id = self.text_loader.load_article(np_id, article.title, article.date, reporter_id)
    #     self.text_loader.load_text(article_id, article.words)

    # def get_article(self, title: str) -> Article:
    #     article_data = self.text_builder.build_entire_text(title)
    #     if article_data:
    #         article = Article(
    #             title=article_data['title'],
    #             authors=f"{article_data['rep_f_name']} {article_data['rep_last_name']}",
    #             date=article_data['date_of_issue'],
    #             content=article_data['content'],
    #             newspaper=article_data['newspaper']
    #         )
    #         article.process_content()  # Reprocess the content to populate the words dictionary
    #         return article
    #     return None

    # def search_articles(self, query: str, search_type: str):
    #     if search_type == 'reporter':
    #         return self.search_wizard.search_reporter_articles(query)
    #     elif search_type == 'newspaper':
    #         return self.search_wizard.search_np_articles(query)
    #     elif search_type == 'date':
    #         return self.search_wizard.search_articles_date(query)
    #     elif search_type == 'word':
    #         return self.search_wizard.search_articles_word(query)
    #     else:
    #         raise ValueError("Invalid search type")
    #
    # def get_word_context(self, article_title: str, word: str):
    #     return self.text_builder.build_context(article_title, word)
    #
    # def get_word_index(self, word: str, article_title: str):
    #     return self.text_builder.build_words_index(word, article_title)
    #
    # def get_all_words(self):
    #     return self.text_builder.all_words()
    #
    # def get_all_words_in_article(self, article_title: str):
    #     article_id = self.db_handler.get_article_id_from_title(article_title)[0][0]
    #     return self.text_builder.all_words_in_article(article_id)
    #
    # def get_word_at_position(self, article_title: str, paragraph: int, line: int, position: int):
    #     return self.search_wizard.search_word_at_position(article_title, paragraph, line, position)
