# Handles text manipulation, file uploading, breaking down words, etc.
import re
from typing import Dict, List, Tuple

# before change:

"""
    def process_content(self):
        paragraphs = self.content.split('\n\n')
        for p_index, paragraph in enumerate(paragraphs, start=1):
            lines = paragraph.split('\n')
            for l_index, line in enumerate(lines, start=1):
                words = re.findall(r'\S+', line)
                spaces = re.findall(r'\s+', line)
                spaces.append('')  # Add an empty string for the last word

                for w_index, (word, space) in enumerate(zip(words, spaces), start=1):
                    clean_word = ''.join(c for c in word if c.isalnum() or c == "'")
                    if clean_word:
                        following_chars = word[len(clean_word):] + space
                        if clean_word not in self.words:
                            self.words[clean_word] = []
                        self.words[clean_word].append((p_index, l_index, w_index, following_chars))

        print("Words dictionary structure!!!!!!!!!!!!!!!!!:")
        for word, positions in self.words.items():
            print(f"{word}: {positions}")
"""


class Article:
    # articles = [Article, Article]
    def __init__(self, txt_file):
        lines = txt_file.split('\n')
        self.title = lines[0].strip()
        self.authors = lines[1].strip()
        self.newspaper = lines[2].strip()
        self.date = lines[3].strip()
        self.content = '\n'.join(lines[4:]).strip()
        self.words: Dict[str, List[Tuple[int, int, int, str]]] = {}

        # Article.articles.append(self)
        print("article created", self.content)
        self.process_content()



    def process_content(self):
        # Split content into paragraphs
        # paragraphs = self.content.split('\n\n')
        # paragraphs = re.split(r'\n\s*\n', self.content.strip())
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', self.content) if p.strip()]

        # self.title = paragraphs[0][0].strip()
        # self.authors = paragraphs[0][1].strip()
        # self.newspaper = paragraphs[0][2].strip()
        # self.date = paragraphs[0][3].strip()
        # self.content = ''.join(paragraphs[1:])


        for p_index, paragraph in enumerate(paragraphs, start=1):
            # Split each paragraph into lines
            lines = paragraph.split('\n')


            for l_index, line in enumerate(lines, start=1):
                # Find all words and spaces in the line
                words = re.findall(r'\S+', line)
                spaces = re.findall(r'\s+', line)
                spaces.append('')  # Add an empty string for the last word

                word_position = 0


                for w_index, word in enumerate(words, start=1):
                    # Clean the word from punctuation and get following characters
                    clean_word = ''.join(c for c in word if c.isalnum() or c == "'")
                    if clean_word:
                        word_position += 1
                        following_chars = word[len(clean_word):] + spaces[w_index - 1]
                        print("word[len(clean_word):]: ", word[len(clean_word):])

                        print("FOLLOWING CHARS", following_chars)
                        if clean_word not in self.words:
                            self.words[clean_word] = []
                        self.words[clean_word].append((p_index, l_index, word_position, following_chars))
        print("Words Dictionary:")
        print("================")
        print(self.get_words_dictionary())
        # for word, occurrences in (self.words.items()):
        #     print(f"Word: '{word}'")
        #     for occurrence in occurrences:
        #         print(
        #             f"  Paragraph: {occurrence[0]}, Line: {occurrence[1]}, Position: {occurrence[2]}, Following chars: '{occurrence[3]}'")
        #     print()  # Empty line for readability between words

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

    def get_words(self):
        return self.words

    # ALSO NEW

    def rebuild_content(self) -> str:
        sorted_words = sorted(
            [(word, pos) for word, positions in self.words.items() for pos in positions],
            key=lambda x: (x[1][0], x[1][1], x[1][2])
        )
        rebuilt_content = ""
        current_para = 0
        for word, (para_num, line_num, _, following_chars) in sorted_words:
            if para_num > current_para:
                rebuilt_content += "\n\n" if current_para > 0 else ""
                current_para = para_num
            rebuilt_content += f"{word}{following_chars}"
        return rebuilt_content.strip()


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



    def show(self):
        print(f'{self.title} by {self.author}')
        print(self.content)
