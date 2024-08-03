# Handles text manipulation, file uploading, breaking down words, etc.
import re
from datetime import *
from TextLoader import *
from typing import Dict, List, Tuple


class Article:
    def __init__(self, txt_file):
        lines = txt_file.split('\n')
        self.title = lines[0].strip()
        self.authors = lines[1].strip()
        self.newspaper = lines[2].strip()
        self.date = lines[3].strip()
        self.content = '\n'.join(lines[4:]).strip()
        self.words: Dict[str, List[Tuple[int, int, int, str]]] = {}
        self.tl = TextLoader()

    def process_content(self):
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', self.content) if p.strip()]
        for p_index, paragraph in enumerate(paragraphs, start=1):
            # Split each paragraph into lines
            lines = paragraph.split('\n')

            for l_index, line in enumerate(lines, start=1):
                # Find all words and spaces in the line
                line = re.sub(r'\r', '', line)
                both = re.findall(r'(\w+\'?\w+)(\W+)(\r)?', line)
                words = [x[0] for x in both]
                spaces = [x[1] for x in both]
                spaces.append('')  # Add an empty string for the last word
                word_position = 0
                for w_index, word in enumerate(words, start=1):
                    # Clean the word from punctuation and get following characters
                    clean_word = ''.join(c for c in word if c.isalnum() or c == "'")
                    if clean_word:
                        word_position += 1
                        following_chars = word[len(clean_word):] + spaces[w_index - 1]
                        if clean_word not in self.words:
                            self.words[clean_word] = []
                        self.words[clean_word].append((p_index, l_index, word_position, following_chars))
        reporter_id = self.tl.load_reporter(self.authors)
        np_id = self.tl.load_newspaper(self.newspaper)
        article_id = self.tl.load_article(np_id, self.title, self.date, reporter_id)
        self.tl.load_text(article_id, self.words)
        print("Words are: ")
        print(self.words)

    def print_words(self):
        print(f"Words Dictionary for article: {self.title}")
        for word, positions in self.words.items():
            print(f"Word: {word}")
            for pos in positions:
                print(f"  Position: (Paragraph: {pos[0]}, Line: {pos[1]}, Word: {pos[2]}), "
                      f"Previous punctuation: '{pos[3]}', Next punctuation: '{pos[4]}'")
            print()  # Empty line for readability

    def get_words_dictionary(self):
        return self.words

    def get_title(self):
        return self.title

    def get_authors(self):
        return self.authors

    def get_newspaper(self):
        return self.newspaper

    def get_date(self):
        return self.date

    def get_content(self):
        return self.content

    def get_words(self):
        return self.words

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
