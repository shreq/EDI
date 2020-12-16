import ftfy
import bs4

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
