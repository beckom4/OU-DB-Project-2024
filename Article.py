# Handles text manipulation, file uploading, breaking down words, etc.
import re
from typing import Dict, List, Tuple

class Article:
    def __init__(self, title: str, authors: str, date: str, content: str, newspaper: str):
        self.title = title
        self.authors = authors
        self.date = date
        self.content = content
        self.newspaper = newspaper
        self.words: Dict[str, List[Tuple[int, int, int, str, str]]] = {}

    def process_content(self):
        paragraphs = self.content.split('\n\n')
        for p_index, paragraph in enumerate(paragraphs, start=1):
            lines = paragraph.split('\n')
            for l_index, line in enumerate(lines, start=1):
                words = re.findall(r'\S+|\s+', line)
                w_index = 0
                prev_punct = ''
                for item in words:
                    if re.match(r'\w+', item):  # It's a word
                        w_index += 1
                        next_punct = words[words.index(item) + 1] if words.index(item) + 1 < len(words) else ''
                        next_punct = next_punct if not re.match(r'\w+', next_punct) else ''
                        if item not in self.words:
                            self.words[item] = []
                        self.words[item].append((p_index, l_index, w_index, prev_punct, next_punct))
                        prev_punct = ''
                    else:  # It's punctuation or whitespace
                        prev_punct += item
        self.print_words()

    def print_words(self):
        print(f"Words Dictionary for article: {self.title}")
        for word, positions in self.words.items():
            print(f"Word: {word}")
            for pos in positions:
                print(f"  Position: (Paragraph: {pos[0]}, Line: {pos[1]}, Word: {pos[2]}), "
                      f"Previous punctuation: '{pos[3]}', Next punctuation: '{pos[4]}'")
            print()  # Empty line for readability


        # Database interaction comment:
        """
        To insert this article into the database:
        1. Use TextLoader.load_reporter(self.authors) to get or create reporter_id
        2. Use TextLoader.load_newspaper(self.newspaper) to get or create np_id
        3. Use TextLoader.load_article(np_id, self.title, self.date, reporter_id) to insert the article
        4. Use TextLoader.load_text(article_id, self.words) to insert the words and their positions
        """

    def rebuild_content(self) -> str:
        sorted_words = sorted(
            [(word, pos) for word, positions in self.words.items() for pos in positions],
            key=lambda x: (x[1][0], x[1][1], x[1][2])
        )
        rebuilt_content = ""
        current_para = 0
        for word, (para_num, line_num, _, prev_punct, next_punct) in sorted_words:
            if para_num > current_para:
                rebuilt_content += "\n\n" if current_para > 0 else ""
                current_para = para_num
            rebuilt_content += f"{prev_punct}{word}{next_punct}"
        return rebuilt_content.strip()

        # Database interaction comment:
        """
        To rebuild the content from the database:
        Use TextBuilder.build_entire_text(self.title) to get the article content
        """

    def get_statistics(self):
        total_words = sum(len(positions) for positions in self.words.values())
        unique_words = len(self.words)
        most_common = sorted(self.words.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        avg_para_length = sum(len(p.split()) for p in self.content.split('\n\n')) / len(self.content.split('\n\n'))
        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "most_common": most_common,
            "avg_para_length": avg_para_length
        }

        # Database interaction comment:
        """
        To get word statistics from the database:
        1. Use TextBuilder.all_words() to get all words in the database
        2. Use TextBuilder.all_words_in_article(article_id) to get all words in a specific article
        3. Use custom queries on the words table to get more detailed statistics
        """

    def search_word(self, word: str):
        # Database interaction comment:
        """
        To search for a word in the database:
        1. Use SearchWizard.search_articles_word(word) to find articles containing the word
        2. Use TextBuilder.build_context(self.title, word) to get the context of the word in this article
        """
        pass

    def get_word_index(self, word: str):
        # Database interaction comment:
        """
        To get the index of a word in the database:
        Use TextBuilder.build_words_index(word, self.title) to get the positions of the word in this article
        """
        pass
    #
    # def __init__(self, title, author, content):
    #     self.title = title
    #     self.author = author
    #     self.content = content
    #
    # def load_from_text(self):
    #     pass
    #
    # def load_from_DB(self):
    #     pass
    #
    #
    def show(self):
        print(f'{self.title} by {self.author}')
        print(self.content)

    # def find_words_before(self, word, number):
    #     pass
    #
    # def find_words_after(self, word, number):
    #     pass
    #
    # def find_words_wrapping(self, word, number):
    #     pass
    #
    # def find_words_count(self, word, number):
    #     pass


