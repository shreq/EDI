import html2text

file = open('concatenate_text.html').read()
txt = html2text.html2text(file)

file = open('concatenate_text.txt', 'w', encoding='utf-8')
file.write(txt)

file.close()
