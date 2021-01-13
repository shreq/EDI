from random import getrandbits
from io import StringIO
import pandas

# load result of clustering (copied from weka to the file)
with open('data/clusters', 'r', encoding='utf-8') as f:
    file = f.read().split('\n')
file = '\n'.join(file[:1] + file[3:])

df = pandas.read_fwf(StringIO(file), index_col='Attribute').drop('Full Data', axis=1)
df.index.name = None

# create random user
user = pandas.Series([bool(getrandbits(1)) for _ in range(df.shape[0])], index=df.index, name='User')

# print comparison
print('Comparison of clusters and user:')
print(pandas.merge(df, user, left_index=True, right_index=True).to_string(), '\n')

# count Jaccard index
similarities = [sum(user & df[col].values) /
                sum(user | df[col].values) for col in df.columns]

# print results
assigned_cluster = str(list(similarities).index(max(similarities)))
print('Similarity to groups:')
for index, value in enumerate(similarities):
    print(f'#{index}: \t{value}')
print(f'Closest group is group #{assigned_cluster}\n')
print('Recommended websites:')
print(df.loc[~user & df[assigned_cluster], assigned_cluster].to_string())
