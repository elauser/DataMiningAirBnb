with open('todo_comprehend.csv', 'r', encoding='utf8') as f:
    counter = 0
    file_lines = []
    for line in f.readlines():
        file_lines.append(f'{counter},{line}')
        counter += 1
    # ''.join([x.strip(), string_to_add, '\n'])
with open('comprehend_indexed.csv', 'w', encoding='utf8') as f:
    f.writelines(file_lines)
