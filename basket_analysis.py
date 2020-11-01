import pandas
import numpy
from mlxtend.frequent_patterns import apriori, association_rules


def to_set(strs) -> set():
    s = set()
    for entry in list(map(str, strs[1:-1].split(', '))):
        s.add(entry[1:-1])
    return s


def to_array(strs) -> []:
    return [entry[1:-1] for entry in list(map(str, strs[1:-1].split(', ')))]


def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


pages = pandas.read_csv('output/popular_sites.csv',
                        usecols=['Site'])['Site'].tolist()
sessions = pandas.read_csv('output/sessions.csv').drop(['Id', 'Start', 'End'], axis=1)
sessions['Time'] = pandas.to_timedelta(sessions['Time'])
sessions['Time/Action'] = pandas.to_timedelta(sessions['Time/Action'])
sessions['Requests'] = sessions['Requests'].apply(to_array)
sessions.drop(['Time', 'Actions_Count', 'Time/Action'], axis=1, inplace=True)

sessions = sessions[[pandas.Series(row).isin(pages).any() for row in sessions['Requests']]]
print(sessions.head(5))
print(sessions.shape)

flags = pandas.DataFrame(index=sessions['User'].unique())

for page in pages:
    flags[page] = [pandas.Series(row).isin([page]).any() for row in sessions.groupby(['User'])['Requests'].sum()]

print(flags)
