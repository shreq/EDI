import pandas
import arff


# read file
df = pandas.read_csv(
    'access_log_Jul95',
    sep=' ',
    header=None,
    na_values='-',
    usecols=[0, 3, 4, 5, 6, 7],
    names=['Address', 'Timestamp', '4', 'Request', 'Response_Code', 'Bytes'],
    dtype='str'
)

# handle timestamps
df['Timestamp'] = df['Timestamp'] + df['4']
df.drop(['4'], axis=1, inplace=True)
df['Timestamp'] = pandas.to_datetime(df['Timestamp'], format='[%d/%b/%Y:%H:%M:%S%z]')
df['Date'] = [d.date() for d in df['Timestamp']]
df['Time'] = [d.time() for d in df['Timestamp']]
df.drop(['Timestamp'], axis=1, inplace=True)
df['Date'] = df['Date'].astype('str')
df['Time'] = df['Time'].astype('str')

# handle bytes
df['Bytes'] = pandas.to_numeric(df['Bytes'], errors='coerce')
df['Bytes'].fillna(0, inplace=True)
df['Bytes'] = df['Bytes'].astype('int64')

# split requests
req = df['Request'].str.split(' ').str
df['Request_Method'], df['Request_Url'] = req[0], req[1]
df.drop('Request', axis=1, inplace=True)

# handle response codes
df['Response_Code'] = pandas.to_numeric(df['Response_Code'], errors='coerce')
df.dropna(inplace=True)
df['Response_Code'] = df['Response_Code'].astype('int64')

# printcheck
print(df.head(5).to_string())
print()
print(df.dtypes)
print()
print(df.isna().sum())

# save results to arff file
print("""
Since arff library does not provide support for python's date format thus "Date" and "Time" have
to be changed manually in arff file from string to: "date YYYY-MM-dd" and "date HH:mm:ss"
""")
df = df.sample(50000, random_state=666)
df = df[['Address', 'Date', 'Time', 'Request_Method', 'Request_Url', 'Response_Code', 'Bytes']]
arff.dump('access_log_Jul95_50k.arff',
          df.values,
          relation='access_log_Jul95_50k',
          names=df.columns)
df.to_csv('access_log_Jul95_50k.csv')
