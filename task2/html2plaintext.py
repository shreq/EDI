import bs4
import pandas
import arff
import ftfy

with open('concatenate_text.html', 'r') as file:
    soup = bs4.BeautifulSoup(file.read(), features='html.parser')

for s in soup(['script', 'style']):
    s.extract()
text = soup.get_text()

lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split('  '))

text = '\n'.join(chunk for chunk in chunks if chunk)
# text = ftfy.fix_text(text)

with open('concatenate_text.txt', 'w', encoding='utf-8') as file:
    file.write(text)

#################################################

with open('concatenate_text.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

text = []
pages = {}
for i, line in enumerate(lines):
    if 'Page ' in line:
        pages[lines[i - 1]] = ' '.join(text[:-1]).replace('\n', ' ')
        text.clear()
        continue
    text.append(line)
# print(pages[u'Powiadomienie [http://ftims.p.lodz.pl/course/view.php?id=3]\n'])

df = pandas.DataFrame(list(pages.keys()), columns=['title'])
df['text'] = list(pages.values())
df.to_csv('pages.csv', index=False)
arff.dump('pages.arff', df.values, relation='pages', names=df.columns)
