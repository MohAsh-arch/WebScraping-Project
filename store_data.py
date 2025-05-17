from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv("clean_data.csv")

engine = create_engine("mysql+mysqlconnector://root:jaT94QLS@localhost:3306/book_store")

df.to_sql("books", con=engine, if_exists="append", index=False)
