import pandas as pd
import arff
from datetime import timedelta

timeout = 1800
percent = 0.5
sessions = []

df = pd.read_csv('output/access_log_Jul95_50k.csv')

# extract users
users = df['Host'].unique()
pd.DataFrame(users).to_csv('output/users.csv', index=False, header=None)

# get sites' count and percent values
sites = df['Request_Url']
sitesCounts = sites.value_counts().rename('Count')
sitesPercents = (sites.value_counts(normalize=True) * 100).rename('Percent')

result = pd.concat([sitesCounts, sitesPercents], axis=1).reset_index().rename(
    {'index': 'Site'}, axis='columns')

# get most popular sites
popularSites = result[result['Percent'] > percent]
pd.DataFrame(popularSites).to_csv(
    'output/popular_sites.csv', index=False, float_format='%.3f')

# concat date and time to extract sessions
df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.drop('Time', axis=1, inplace=True)

# extract sessions
for user in users:
    requests = df[df['Host'] == user]
    start = requests.iloc[0]['Date']
    end = start
    sessionRequests = []
    popularSitesFlags = {value: False for value in popularSites['Site']}

    for index, req in requests.iterrows():
        if req['Date'] - start > timedelta(seconds=timeout):
            if len(sessionRequests) > 1:
                time = (end - start).total_seconds()
                actionsCount = len(sessionRequests)
                timePerAction = time/(actionsCount - 1)

                sessions.append({**{'User': user, 'Time': time, 'Actions_Count': actionsCount,
                                    'Time_Per_Action': timePerAction,
                                    'Requests': sessionRequests}, **popularSitesFlags})
            popularSitesFlags = {
                value: False for value in popularSites['Site']}
            sessionRequests = []
            start = req['Date']

        sessionRequests.append(req['Request_Url'])
        end = req['Date']

        if req['Request_Url'] in popularSitesFlags:
            popularSitesFlags[req['Request_Url']] = True

sessions = pd.DataFrame(sessions)
print(sessions.head(5))

# user-site flags
userFlags = pd.DataFrame(index=sessions['User'].unique())
for site in popularSites['Site']:
    userFlags[site] = [(site in row) for row in sessions.groupby(['User'])['Requests'].sum()]
userFlags[:] = userFlags[:].astype('object')
print(userFlags)

userFlags.to_csv('output/hostflags.csv', index=False)
arff.dump('output/hostflags.arff',
          userFlags.values,
          relation='hostflags',
          names=userFlags.columns)

# discretization
quantile33 = sessions.iloc[:, 1:4].quantile(0.33)
quantile66 = sessions.iloc[:, 1:4].quantile(0.66)
for column in sessions.iloc[:, 1:4].columns:
    sessions[column] = sessions[column].apply(lambda row:
        'Low' if row < quantile33[column] else 'Medium' if row < quantile66[column] else 'High'
    )

# sessions save
sessions.drop('Requests', axis=1, inplace=True)

print("""
Columns Time, Actions_Count and Time_Per_Actions are discretized and to
make them suitable for weka their format needs to be changed manually
in arff file from string to {Low, Medium, High}
""")
sessions.to_csv('output/sessions.csv', index=False)
sessions[sessions.columns[5:]] = sessions[sessions.columns[5:]].astype(object)
arff.dump('output/sessions.arff',
          sessions.values,
          relation='sessions',
          names=sessions.columns)
