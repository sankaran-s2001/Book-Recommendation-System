import streamlit as st
import pickle
import numpy as np
import pandas as pd


def set_background_image(image_file):
    import base64
    
    with open(image_file, "rb") as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data).decode()
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                          url("data:image/jpg;base64,{img_base64}");
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Make text white and readable */
    .stApp, .main, h1, h2, h3, p {{
        color: white !important;
    }}
    
    /* Style content containers */
    .main .block-container {{
        background: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: rgba(0, 0, 0, 0.7);
        color: white !important;
    }}
    
    </style>
    """, unsafe_allow_html=True)

set_background_image('background_image.jpg')



# Load saved models
@st.cache_data
def load_models():
    # Base URL to Hugging Face repo files
    base_url = "https://huggingface.co/sankarans2001/Book-Recommendation-System/resolve/main/"
    
    def load_pickle_from_url(filename):
        url = base_url + filename
        response = requests.get(url)
        response.raise_for_status()  # Throw error if request failed
        return pickle.loads(response.content)
    
    popular_df = load_pickle_from_url('popular.pkl')
    pt = load_pickle_from_url('pt.pkl')
    books = load_pickle_from_url('books.pkl')
    similarity_scores = load_pickle_from_url('similarity_scores.pkl')
    
    return popular_df, pt, books, similarity_scores

# Load models
popular_df, pt, books, similarity_scores = load_models()

# Recommendation function
def recommend(book_name):
    if book_name not in pt.index:
        return []
    
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), 
                          key=lambda x: x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        item.append(i[1])
        
        data.append(item)
    
    return data

# Streamlit App
st.set_page_config(page_title="📚 Book Recommendation System", layout="wide")

# Header
st.title("📚 Book Recommendation System")
st.markdown("*Discover your next favorite book with ML-powered recommendations!*")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Choose Recommendation Type:", 
                           ["🏆 Popular Books", "🤝 Personalized Recommendations"])

st.sidebar.markdown("---")

st.sidebar.markdown("**💡 How it works:**")

st.sidebar.markdown("""
    **🏆 Popular Books:**
    - Based on ratings from 1000+ expert readers
    - Books with 150+ ratings and highest scores
    - Perfect for discovering universally loved books
    """)
st.sidebar.markdown("---")

st.sidebar.markdown("""
    **🤝 Personalized Recommendations:**
    - ML analyzes reading patterns of similar users
    - Finds books with similar rating patterns
    - Collaborative filtering with 220 carefully selected books
    """)

# Popular Books Page
if page == "🏆 Popular Books":
    st.header("🏆 Top 50 Most Popular Books")
    st.markdown("*These books are loved by readers worldwide!*")
    
    # Display popular books in a nice grid
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i in range(len(popular_df)):
        book = popular_df.iloc[i]
        
        # Rotate through columns
        if i % 5 == 0:
            with col1:
                st.image(book['Image-URL-M'], width=120)
                st.write(f"**{book['Book-Title'][:30]}...**")
                st.write(f"*by {book['Book-Author']}*")
                st.write(f"⭐ {book['avg_rating']:.1f} ({book['num_ratings']} ratings)")
                st.markdown("---")
        elif i % 5 == 1:
            with col2:
                st.image(book['Image-URL-M'], width=120)
                st.write(f"**{book['Book-Title'][:30]}...**")
                st.write(f"*by {book['Book-Author']}*")
                st.write(f"⭐ {book['avg_rating']:.1f} ({book['num_ratings']} ratings)")
                st.markdown("---")
        elif i % 5 == 2:
            with col3:
                st.image(book['Image-URL-M'], width=120)
                st.write(f"**{book['Book-Title'][:30]}...**")
                st.write(f"*by {book['Book-Author']}*")
                st.write(f"⭐ {book['avg_rating']:.1f} ({book['num_ratings']} ratings)")
                st.markdown("---")
        elif i % 5 == 3:
            with col4:
                st.image(book['Image-URL-M'], width=120)
                st.write(f"**{book['Book-Title'][:30]}...**")
                st.write(f"*by {book['Book-Author']}*")
                st.write(f"⭐ {book['avg_rating']:.1f} ({book['num_ratings']} ratings)")
                st.markdown("---")
        else:
            with col5:
                st.image(book['Image-URL-M'], width=120)
                st.write(f"**{book['Book-Title'][:30]}...**")
                st.write(f"*by {book['Book-Author']}*")
                st.write(f"⭐ {book['avg_rating']:.1f} ({book['num_ratings']} ratings)")
                st.markdown("---")

# Personalized Recommendations Page
else:
    st.header("🤝 Get Personalized Book Recommendations")
    st.markdown("*Tell us a book you liked, and we'll find similar ones!*")
    
    # Book selection dropdown
    book_list = pt.index.values
    selected_book = st.selectbox(
        "Choose a book you enjoyed:",
        book_list,
        help="Select a book from our database to get personalized recommendations"
    )
    
    # Recommendation button
    if st.button("📖 Get Recommendations", type="primary"):
        with st.spinner("Finding similar books..."):
            recommendations = recommend(selected_book)
        
        if recommendations:
            st.success(f"📚 Books similar to **{selected_book}**:")
            st.markdown("---")
            
            # Display recommendations in a clean layout
            for i, (title, author, year, publisher, image, similarity_score) in enumerate(recommendations, 1):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    try:
                        st.image(image, width=150)
                    except:
                        st.image("https://via.placeholder.com/150x200?text=No+Image", width=150)
                
                with col2:
                        st.markdown(f"### {i}. {title}")
                        st.markdown(f"**📝 Author:** {author if author else 'Unknown Author'}")
                        
                        # Handle missing year
                        year_display = year if year and str(year) != 'nan' else 'Unknown Year'
                        st.markdown(f"**📅 Year:** {year_display}")
                        
                        # Handle missing publisher
                        publisher_display = publisher if publisher and str(publisher) != 'nan' else 'Unknown Publisher'
                        st.markdown(f"**🏢 Publisher:** {publisher_display}")
                        
                        # Similarity score with progress bar
                        similarity_percentage = similarity_score * 100
                        st.markdown(f"**📊 Similarity Score:** {similarity_percentage:.1f}%")

                
                st.markdown("---")
        else:
            st.error("❌ Sorry, couldn't find recommendations for this book.")

# Footer
st.markdown("---")
st.markdown("*✨Created by Sankaran S*")

