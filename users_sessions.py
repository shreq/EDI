import pandas as pd
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

    for index, req in requests.iterrows():
        if req['Date'] - start > timedelta(seconds=timeout):
            sessions.append({'User': user, 'Start': start,
                             'End': end, 'Requests': sessionRequests})
            sessionRequests = []
            start = req['Date']

        sessionRequests.append(req['Request_Url'])
        end = req['Date']

#
sessions = pd.DataFrame(sessions)
sessions['Time'] = (sessions['End'] - sessions['Start']).apply(lambda x: x.total_seconds())
sessions['Actions_Count'] = sessions['Requests'].str.len()
sessions['Time_Per_Action'] = sessions['Time'] / (sessions['Actions_Count'] - 1)
print(sessions.head(5))

pd.DataFrame(sessions).to_csv('output/sessions.csv', index_label='Id')
