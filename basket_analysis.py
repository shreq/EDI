import pandas
import datetime
import arff


def to_array(strs) -> []:
    return [entry[1:-1] for entry in list(map(str, strs[1:-1].split(', ')))]


def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1


# load sessions and sites
pages = pandas.read_csv('output/popular_sites.csv',
                        usecols=['Site'])['Site'].tolist()
sessions = pandas.read_csv('output/sessions.csv').drop(['Id', 'Start', 'End'], axis=1)
sessions['Requests'] = sessions['Requests'].apply(to_array)

# drop sessions with unpopular sites only
sessions = sessions[[pandas.Series(row).isin(pages).any() for row in sessions['Requests']]]

# prepare flags
flags = pandas.DataFrame(index=sessions['User'].unique())
for page in pages:
    flags[page] = [pandas.Series(row).isin([page]).any() for row in sessions.groupby(['User'])['Requests'].sum()]
    flags[page] = flags[page].astype('int64')

# requests aren't needed anymore
sessions.drop(['Requests'], axis=1, inplace=True)

# printcheck
print(sessions.head(5))
print()
print(flags.head(5))

# save results
sessions.to_csv('output/sessions2.csv', index=False)
flags.to_csv('output/flags.csv', index=False)

arff.dump('output/sessions2.arff',
          sessions.values,
          relation='sessions',
          names=sessions.columns)
arff.dump('output/flags.arff',
          flags.values,
          relation='flags',
          names=flags.columns)
