import pandas as pd 



df = pd.read_csv('raw_data.csv')
df.drop_duplicates(inplace = True) 



clean_data = df
clean_data['price'] = clean_data['price'].str.replace('£','').astype(float)

ratings_dict = {
    'One':   1,
    'Two':   2,
    'Three': 3,
    'Four':  4,
    'Five':  5
}

clean_data['rating'] = clean_data['rating'].map(ratings_dict)

clean_data.to_csv('clean_data.csv', index=False)