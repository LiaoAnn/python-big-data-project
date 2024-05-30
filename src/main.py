import pandas as pd

# Load data
ratings = pd.read_csv('./ml-latest-small/ratings.csv')
movies = pd.read_csv('./ml-latest-small/movies.csv')
moviesDf = pd.DataFrame(movies)

# Merge the two dataframes
movies_data = pd.merge(ratings, movies, on='movieId')
ratings_mean_count = pd.DataFrame(movies_data.groupby('title')['rating'].mean())
ratings_mean_count['rating_counts'] = pd.DataFrame(movies_data.groupby('title')['rating'].count())

# Create a pivot table
user_movie_rating = movies_data.pivot_table(index='userId', columns='title', values='rating')

def get_similar_movies(movie_name):
    movie_ratings = user_movie_rating[movie_name]

    # 確保數據中沒有缺失值，並填充NaN為0（或使用其他適合的值）
    movie_ratings = movie_ratings.fillna(0)
    user_movie_rating_filled = user_movie_rating.fillna(0)

    similar_movies = user_movie_rating_filled.corrwith(movie_ratings)
    corr_movie = pd.DataFrame(similar_movies, columns=['Correlation'])
    corr_movie.dropna(inplace=True) # 刪除NaN值
    corr_movie = corr_movie.join(ratings_mean_count)
    return corr_movie[corr_movie['rating_counts'] > 50].sort_values('Correlation', ascending=False).head()

def search_movies(query):
    results = moviesDf[moviesDf['title'].str.contains(query, case=False, na=False)]
    return results

def get_movie_id(movie_name):
    return movies[movies['title'] == movie_name]['movieId'].values[0]

def get_movie_name_by_id(movie_id):
    return movies[movies['movieId'] == movie_id]['title'].values[0]

def main():
    while True:
        query = input("請輸入電影名稱 (或輸入 'exit' 離開): ")
        if query.lower() == 'exit':
            print("已退出查詢系統。")
            break
        results = search_movies(query)
        if not results.empty:
            print("查詢結果:")
            print(results)
            print("如果找到您要的電影，請紀錄該電影的 movieId 以便查詢相似電影。")
        else:
            print("未找到相關電影。")

    movie_id = input("請輸入電影的 movieId: ")
    movie_name = get_movie_name_by_id(int(movie_id))
    print(f"您選擇的電影是: {movie_name}")
    similar_movies = get_similar_movies(movie_name)
    print("相似電影:")
    print(similar_movies)

if __name__ == "__main__":
    main()
