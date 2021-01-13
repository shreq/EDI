from random import getrandbits
from numpy import array
import pandas

# load result of clustering (copied from weka to the file)
df = pandas.read_fwf('data/clusters', index_col='Attribute').drop('Full Data', axis=1)

# create random user
user = array([bool(getrandbits(1)) for _ in range(df.shape[0])])
# user = array([True, True,  True, False, False, False, False, False, False, False, False, False,
#               False, False, False, False, False, False, False, False, False, False, False, False,
#               False, False, False, False])
# df['User'] = user
# print(df.to_string())
# df.drop('User', axis=1, inplace=True)

# count Jaccard index
similarities = []
for col in df.columns:
    union = user | df[col].values
    intersection = user & df[col].values
    similarities.append(sum(intersection) / sum(union))

# print recommended sites
assigned_cluster = str(list(similarities).index(max(similarities)))
print(df.loc[~user & df[assigned_cluster], assigned_cluster])
