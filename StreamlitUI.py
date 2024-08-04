import streamlit as st
from DB_handler import *
from TextBuilder import *
from Article import Article
from datetime import *
from SearchWizard import *
import pandas as pd


def parse_date(date_str_inp):
    try:
        # Try to parse the date string using the specified format
        ret = datetime.strptime(date_str_inp, '%B %d, %Y')
        return ret
    except ValueError:
        # If a ValueError is raised, the date string does not match the format
        return None


class StreamlitUI:
    def __init__(self, database: DB_handler):
        self.database = database
        self.sw = SearchWizard()
        seld.tb = TextBuilder()

    def run(self):
        st.title("News Article Database")

        menu = ["Home", "Add Article", "Search Articles", "View Article", "Word Statistics", "Print Words Dictionary"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Home":
            self.show_home()
        elif choice == "Add Article":
            self.add_article()
        elif choice == "Search Articles":
            self.search_articles()
        elif choice == "View Article":
            self.view_article()
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
                    print("Article processed")
                    st.success("Article added successfully!")
            except Exception as e:
                st.error('Error processing file. It is possible that the article is already in the system.')
        else:
            st.write("Please upload a .txt file to add an article.")

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
                df = pd.DataFrame(articles_of_newspaper, columns=["Article Title" , "Date"])
                st.subheader(f"Articles in {newspaper_name}: ")
                st.dataframe(df, hide_index=True)
            elif articles_of_newspaper is not None and len(articles_of_newspaper) == 0:
                st.write("No articles found.")
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

    def view_article(self):
        st.subheader("View Article")
        title = st.text_input("Enter article title")

        if st.button("View"):
            article = self.database.get_article(title)
            if article:
                st.write(f"Title: {article.title}")
                st.write(f"Authors: {article.authors}")
                st.write(f"Date: {article.date}")
                st.write(f"Newspaper: {article.newspaper}")
                st.write("Content:")
                st.write(article.content)
            else:
                st.write("Article not found.")

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
