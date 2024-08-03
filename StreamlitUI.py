import streamlit as st
from DB_handler import *
from TextLoader import *
from Article import Article
from datetime import *
import re

from SearchWizard import *


def parse_date(date_str_inp):
    # Remove the ordinal suffix
    # Parse the date
    date_obj = datetime.strptime(date_str_inp, "%B %d, %Y")
    return date_obj


class StreamlitUI:
    def __init__(self, database: DB_handler):
        self.database = database
        self.sw = SearchWizard()

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
                article_text = uploaded_file.read().decode('utf-8')
                lines = article_text.split('\n')

                title = lines[0].strip()
                authors = lines[1].strip()
                date_art = lines[2].strip()
                newspaper = st.text_input("Newspaper", value=uploaded_file.name.split('.')[0])
                content = '\n'.join(lines[3:])

                st.write(f"Title: {title}")
                st.write(f"Authors: {authors}")
                st.write(f"Date: {date_art}")
                st.write(f"Newspaper: {newspaper}")
                st.write("Content Preview:")
                st.write(content[:500] + "...")  # Show first 500 characters

                if st.button("Add Article"):
                    try:
                        date_obj = parse_date(date_art)
                    except ValueError:
                        st.error("Invalid date format. Please use YYYY-MM-DD.")
                        return

                    article = Article(title, authors, date_obj, content, newspaper)
                    article.process_content()
                    print("Article processed")
                    st.success("Article added successfully!")

            except Exception as e:
                st.error(f'Error processing file: {str(e)}')
        else:
            st.write("Please upload a .txt file to add an article.")

    def search_articles(self):
        st.subheader("Search Articles")
        search_type = st.selectbox("Search article by", ["", "reporter", "newspaper", "date", "word"])

        if search_type == "reporter":
            reporter_name = st.text_input("Please enter a reporter's name: ")
            articles_of_reporter = self.sw.search_reporter_articles(reporter_name)
            if articles_of_reporter is not None:
                st.write(f"Articles written by the {reporter_name}: ")
                st.table(articles_of_reporter)
            else:
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
