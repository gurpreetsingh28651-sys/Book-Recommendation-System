import streamlit as st
import pickle

#load
books = pickle.load(open('books.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.set_page_config(page_title="Book Recommender", layout="wide")

#css
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.header {
    font-size: 45px;
    font-weight: bold;
    color: white;
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

.card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 15px;
    margin: 10px;
    text-align: center;
    transition: 0.3s;
    color: white;
}

.card:hover {
    transform: scale(1.07);
    background-color: #262730;
}

.small-text {
    color: #bbbbbb;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

#header
st.markdown("<div class='header'>📚 Smart Book Recommender</div><br>", unsafe_allow_html=True)

#sidebar
st.sidebar.title("⚙ Filters")

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + list(books['genre'].dropna().unique())
)

selected_author = st.sidebar.selectbox(
    "Select Author",
    ["All"] + list(books['author'].dropna().unique())
)

#filter
filtered_books = books.copy()

if selected_genre != "All":
    filtered_books = filtered_books[filtered_books['genre'] == selected_genre]

if selected_author != "All":
    filtered_books = filtered_books[filtered_books['author'] == selected_author]

#search
selected_book = st.selectbox("🔍 Search Book", filtered_books['title'].values)

#recommend
def recommend(book_name):
    index = books[books['title'] == book_name].index[0]
    distances, indices = model.kneighbors(model._fit_X[index], n_neighbors=6)

    rec_books = []
    for i in indices[0][1:]:
        rec_books.append(books.iloc[i])
    return rec_books

#button
if st.button("🚀 Recommend"):
    results = recommend(selected_book)

    st.subheader("✨ Recommended Books")

    cols = st.columns(5)

    for i, book in enumerate(results):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                📖 <br><br>
                <b>{book['title']}</b><br><br>
                <div class='small-text'>✍ {book['author']}</div>
                <div class='small-text'>📚 {book['genre']}</div>
            </div>
            """, unsafe_allow_html=True)