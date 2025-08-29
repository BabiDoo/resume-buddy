from tika import parser

file = 'my_file.pdf'

#Parsing
data = parser.from_file(file)

# Extracting text
text = data['content']


with open('meu_arquivo.txt', 'w', encoding='utf-8') as f:
    f.write(text if text else "")