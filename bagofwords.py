import pandas as pd
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('cleandata.csv')
df.drop('date', inplace=True, axis=1)
df['location']=df['location'].replace('Delhi','New Delhi')
df['vertical'] = df['vertical'].apply(lambda x: x.split())

df['location'] = df['location'].apply(lambda x: x.split())
df['investment_type'] = df['investment_type'].apply(lambda x: x.split())
df['startup'] = df['startup'].apply(lambda x: x.split())
df['tags'] = df['startup'] + df['vertical'] + df['investment_type']


df1 = df[['investor','tags']]


df1 = df1.copy()
df1['tags'] = df1['tags'].apply(lambda x: " ".join(x))

df1['tags'] = df1['tags'].apply(lambda x: x.lower())

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

df1['tags'] = df1['tags'].apply(stem)

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(df1['tags']).toarray()

similarity = cosine_similarity(vectors)

def similar_investor(investors):
    investor_index = df1[df1['investor'] == investors].index[0]
    distances = similarity[investor_index]
    investor_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    result = [df1.iloc[i[0]].investor for i in investor_list]
    return result





