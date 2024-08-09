from text_highlighter import text_highlighter
from streamlit_annotation_tools import text_highlighter

import streamlit as st
from Article import Article
from datetime import *
from SearchWizard import *
from TextBuilder import *
from WordGroup import *
import pandas as pd


def parse_date(date_str_inp):
    try:
        # Try to parse the date string using the specified format
        ret = datetime.strptime(date_str_inp, '%B %d, %Y')
        return ret
    except ValueError:
        # If a ValueError is raised, the date string does not match the format
        return None


def make_arr_from_tuparr(tup_arr):
    ret = []
    for tup in tup_arr:
        ret.append(tup[0])
    return ret


class StreamlitUI:
    def __init__(self, database: DB_handler):
        self.database = DB_handler()
        self.sw = SearchWizard()
        self.tb = TextBuilder()
        self.wg = WordGroup()

    def run(self):
        st.title("News Article Database")

        menu = ["Home", "Add Article", "Search", "View", "Word groups", "Word Statistics", "Print Words Dictionary"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            self.show_home()
        elif choice == "Add Article":
            self.add_article()
        elif choice == "Search":
            self.search()
        elif choice == "View":
            self.view()
        elif choice == "Word groups":
            self.word_groups()
        elif choice == "Word Statistics":
            self.word_statistics()
        elif choice == "Print Words Dictionary":
            self.print_words_dictionary()

    def show_home(self):
        st.write("Welcome to the News Article Database!")
        st.write("Use the sidebar to navigate through different functions.")

    def add_article(self):
        st.subheader("Add a New Article")

        uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

        if uploaded_file is not None:
            try:
                full_text_file = uploaded_file.read().decode('utf-8')
                article = Article(full_text_file)
                st.write(f"Title: {article.get_title()}")
                st.write(f"Authors: {article.get_authors()}")
                st.write(f"Newspaper name: {article.get_newspaper()}")
                st.write(f"Date: {article.get_date()}")
                st.write("--------------------")
                st.write("Content Preview:")
                st.write(article.get_content())
                if st.button("Add Article"):
                    article.process_content()
                    st.success("Article added successfully!")
            except Exception as e:
                st.error('Error processing file. It is possible that the article is already in the system.')
        else:
            st.write("Please upload a .txt file to add an article.")

    def search(self):
        st.subheader("Search")
        search_type = st.selectbox("What would you like to search for?", ["Please select", "Article", "Word", ])
        if search_type == "Article":
            self.search_articles()
        elif search_type == "Word":
            self.search_word()

    def search_articles(self):
        st.subheader("Search Articles")
        search_type = st.selectbox("Search article by", ["Please select", "reporter", "newspaper", "date", "word"])

        if search_type == "reporter":
            reporter_name = st.text_input("Please enter a reporter's name: ")
            articles_of_reporter = self.sw.search_reporter_articles(reporter_name)
            if articles_of_reporter is not None and len(articles_of_reporter) != 0:
                df = pd.DataFrame(articles_of_reporter, columns=["Article Title", "Newspaper", "Date"])
                st.subheader(f"Articles written by {reporter_name}: ")
                st.dataframe(df, hide_index=True)
            elif articles_of_reporter is not None and len(articles_of_reporter) == 0:
                st.write("No articles found.")
        elif search_type == "newspaper":
            newspaper_name = st.text_input("Please enter a newspaper's name: ")
            articles_of_newspaper = self.sw.search_np_articles(newspaper_name)
            if articles_of_newspaper is not None and len(articles_of_newspaper) != 0:
                df = pd.DataFrame(articles_of_newspaper, columns=["Article Title", "Date"])
                st.subheader(f"Articles in {newspaper_name}: ")
                st.dataframe(df, hide_index=True)
            elif articles_of_newspaper is not None and len(articles_of_newspaper) == 0:
                st.write("No articles found.")
            elif articles_of_newspaper is None and len(newspaper_name) != 0:
                st.write("Invalid newspaper")
        elif search_type == "date":
            date_str = st.text_input("Please enter a date (e.g. January 1, 2022): ")
            if len(date_str) != 0:
                p_date = parse_date(date_str)
                if p_date is not None:
                    articles_of_date = self.sw.search_articles_date(p_date)
                    if articles_of_date is not None and len(articles_of_date) != 0:
                        df = pd.DataFrame(articles_of_date, columns=["Article Title", "Newspaper"])
                        st.subheader(f"Articles published on {date_str}: ")
                        st.dataframe(df, hide_index=True)
                    elif articles_of_date is not None and len(articles_of_date) == 0:
                        st.write("No articles found.")
                else:
                    st.write("Invalid date format. Please enter a date in the format 'Month day, year'.")
        elif search_type == "word":
            word = st.text_input("Please enter a word: ")
            articles_of_word = self.sw.search_articles_word(word)
            if articles_of_word is not None and len(articles_of_word) != 0:
                df = pd.DataFrame(articles_of_word, columns=["Article Title", "Newspaper", "Date"])
                st.subheader(f"Articles containing the word '{word}': ")
                st.dataframe(df, hide_index=True)
            elif articles_of_word is not None and len(articles_of_word) == 0:
                st.write("No articles found.")

    def search_word(self):
        st.subheader("Search Word")
        article_title = st.text_input("Enter article title")
        paragraph_number = st.text_input("Enter paragraph number")
        line_number = st.text_input("Enter line number")
        position_in_line = st.text_input("Enter position in line")
        if st.button("Search"):
            if len(article_title) != 0 and len(paragraph_number) != 0 and len(line_number) != 0 and len(
                    position_in_line) != 0:
                word = self.sw.search_word_at_position(article_title, paragraph_number, line_number, position_in_line)
                if word:
                    st.write(
                        f"The word at position ({paragraph_number}, {line_number}, {position_in_line}) in the article '{article_title}' is: {word}")
                else:
                    st.write("Word not found.")
            else:
                st.write("Please fill all fields.")

    def view(self):
        st.subheader("View")
        view_type = st.selectbox("What do you want to view?",
                                 ["Please select", "Article", "All words in db", "All words in article",
                                  "Index of all words in article"])
        if view_type == "Article":
            article_title = st.text_input("Enter article title")
            if st.button("View"):
                article = self.tb.build_entire_text(article_title)
                if article:
                    st.write(f"Title: {article[0]}")
                    st.write(f"Date: {article[1]}")
                    st.write(f"Reporter: {article[2]}")
                    st.write("Content:")
                    st.write(article[3])
                else:
                    st.write("Article not found.")
        elif view_type == "All words in db":
            words = self.tb.all_words()
            if words:
                st.subheader("All the words in the database are: ")
                for word_tup in words:
                    st.write(word_tup[0])
                st.write(words)
            else:
                st.write("The database has no words yet.")
        elif view_type == "All words in article":
            article_title = st.text_input("Enter article title")
            if st.button("View"):
                words = self.tb.all_words_in_article(article_title)
                if words:
                    st.subheader(f"All the words in the article '{article_title}' are: ")
                    for word_tup in words:
                        st.write(word_tup[0])
                elif article_title and words is None:
                    st.write("The article is empty")
                else:
                    st.write("Article not found.")
        elif view_type == "Index of all words in article":
            article_title = st.text_input("Enter article title")
            if st.button("View") and article_title:
                words_index = self.tb.build_words_index(article_title)
                if len(article_title) != 0 and words_index is None:
                    st.write("Invalid article title")
                elif words_index:
                    df = pd.DataFrame(words_index, columns=["Word", "Index"])
                    st.subheader(f"The words index in the article '{article_title}': ")
                    st.write("* Please note that the index is a paragraph number, row number and position in the row")
                    st.dataframe(df, hide_index=True, width=1000)
                elif article_title and words_index is None:
                    st.write("The article is empty")
                else:
                    st.write("Article not found.")

    def word_groups(self):
        st.subheader("Word Groups")
        wg_type = st.selectbox("What would you like to do?",
                               ["Please select", "Create group", "Add word to existing group", "My groups"])
        if wg_type == "Create group":
            group_description = st.text_input("Enter group description")
            group_id = self.wg.get_group_id(group_description)
            if group_id and st.button("Create group") and len(group_description) != 0:
                st.error("Group already exists.")
            elif group_id is None and st.button("Create group") and len(group_description) != 0:
                try:
                    self.wg.create_group(group_description)
                    st.success(f"Group {group_description} created successfully.\n "
                               f" Please check out the 'Add word to existing group' option to add words to the group.")
                except Exception as e:
                    st.error("Error while creating the group.")
        elif wg_type == "Add word to existing group":
            group_description = st.text_input("Enter group description")
            group_id = self.wg.get_group_id(group_description)
            # if st.button("Continue"):
            if group_id:
                add_type = st.selectbox("How would you like to add the word to the group?",
                                        ["Please select", "Type word", "Select from a list of words"])
                if add_type == "Type word":
                    word = st.text_input("Please enter the word you would like to add to the group.")
                    word_id = self.database.get_word_id_from_word(word)
                    is_in_group = self.wg.is_word_in_group(group_id, word_id)
                    if is_in_group:
                        st.error(f"The word {word} is already in the group.")
                    else:
                        if st.button("Add word to group"):
                            if word_id == -1:
                                st.error("The word you're trying to enter is not any of the articles.")
                            else:
                                try:
                                    self.wg.add_word_to_group(group_id, word_id)
                                    st.success(f"The word {word} has been added to the list.")
                                except Exception as e:
                                    st.error("Error while adding the word to the group.")
                elif add_type == "Select from a list of words":
                    word_options = ["Please select"]
                    word_options.extend(make_arr_from_tuparr(self.tb.all_words()))
                    word = st.selectbox(f"Which word would you like to add to the group {group_description}?",
                                        word_options)
                    if word != "Please select":
                        word_id = self.database.get_word_id_from_word(word)
                        is_in_group = self.wg.is_word_in_group(group_id, word_id)
                        if is_in_group:
                            st.error(f"The word {word} is already in the group.")
                        else:
                            if word_id == -1:
                                st.error("The word you're trying to enter is not any of the articles.")
                            else:
                                try:
                                    self.wg.add_word_to_group(group_id, word_id)
                                    st.success(f"The word {word} has been added to the list.")
                                except Exception as e:
                                    st.error("Error while adding the word to the group.")
            elif not group_id and group_description:
                st.error("Group not found.")
        elif wg_type == "My groups":
            groups = ["Please select"]
            groups.extend(make_arr_from_tuparr(self.wg.get_all_groups()))
            group = st.selectbox("My groups:", groups)
            if group != "Please select":
                words = self.wg.get_group(group)
                if words:
                    st.subheader(f"Words in group {group}:")
                    for word in words:
                        st.write(word)
                else:
                    st.write("Group is empty.")

    def word_statistics(self):
        st.subheader("Word Statistics")
        title = st.text_input("Enter article title (leave blank for all articles)")

        if st.button("Get Statistics"):
            if title:
                words = self.database.get_all_words_in_article(title)
                st.write(f"Words in article '{title}':")
            else:
                words = self.database.get_all_words()
                st.write("Words in all articles:")

            word_counts = {}
            for word in words:
                if word[0] in word_counts:
                    word_counts[word[0]] += 1
                else:
                    word_counts[word[0]] = 1

            sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            for word, count in sorted_words[:20]:
                st.write(f"{word}: {count}")

    def print_words_dictionary(self):
        st.subheader("Print Words Dictionary")
        title = st.text_input("Enter article title")

        if st.button("Print Words Dictionary"):
            article = self.database.get_article(title)
            if article:
                st.write(f"Words Dictionary for article: {article.title}")
                st.text_area("Words Dictionary", article.print_words_dictionary(), height=400)
            else:
                st.write("Article not found.")
