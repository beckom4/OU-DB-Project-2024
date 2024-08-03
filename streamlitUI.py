import streamlit as st

from article import Article
from database import Database
from article import Article
import datetime


class StreamlitUI:
    def __init__(self, database: Database):
        self.database = database

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
                print("text uploadedd!")
                print("got to this point1")
                article = Article(full_text_file)


                # article.process_content()
                # paragraphs = article_text.split('\n\n')
                #
                # title = paragraphs[0][0].strip()
                # authors = paragraphs[0][1].strip()
                # newspaper = paragraphs[0][2].strip()
                # date = paragraphs[0][3].strip()
                # content = ''.join(paragraphs[1:])
                #
                # for p_index, paragraph in enumerate(paragraphs, start=1):
                #     # Split each paragraph into lines
                #     lines = paragraph.split('\n')

                # print('TITLE:', article.get_title())
                # print('AUTHOR:', article.get_authors())
                # print('NEWSPAPER:', article.get_newspaper())
                # print('DATE:', article.get_date())
                # print('CONTENT:', article.get_content())

                st.write(f"Title: {article.get_title()}")
                st.write(f"Authors: {article.get_authors()}")
                st.write(f"Newspaper name: {article.get_newspaper()}")
                st.write(f"Date: {article.get_date()}")
                st.write("--------------------")
                st.write("Content Preview:")
                st.write(article.get_content())
                # st.write("Words Dictionary:", article.get_words())


                # LOWER BUTTON- TO ADD ANDDITIONAL ONE:
                # if st.button("Add Article"):
                #     print("ADD ARTICLE BUTTON PRESSED")
                #     try:
                #         # date_obj = datetime.datetime.strptime(article.get_date(), "%Y-%m-%d").date()
                #         article = Article()
                #         print("got to this point2")
                #         article.process_content()
                #         print('BEFORE DATABASE')
                #         self.database.add_article(article)
                #         print("AFTER DATABASE")
                #         st.success("Article added successfully!")
                #     except ValueError:
                #         st.error(
                #             "Invalid date format. The date in the txt file should be in YYYY-MM-DD format (e.g., 2023-05-25).")

            except Exception as e:
                print('EXCEPTION FROM add_article')
                st.error(f'Error processing file: {str(e)}')
        else:
            st.write("Please upload a .txt file to add an article.")


    def search_articles(self):
        st.subheader("Search Articles")
        search_type = st.selectbox("Search by", ["reporter", "newspaper", "date", "word"])
        query = st.text_input("Enter search query")


        if st.button("Search") and len(query) > 0:
            results = self.database.search_articles(query, search_type)
            if results:
                for result in results:
                    st.write(f"- {result[0]} ({result[1]})")
            else:
                st.write("No articles found.")

    def view_article(self):
        st.subheader("View Article")
        title = st.text_input("Enter article title")

        if st.button("View"):
            # article = self.database.get_article(title)
            if article:
                st.write(f"Title: {article.get_title()}")
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