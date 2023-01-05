import json

words_list = []

with open('censored_words.txt', encoding='utf-8') as file:
    for i in file:
        row = i.lower().split('\n')[0]
        if row != '':
            words_list.append(row)

with open('censored_words.json', "w", encoding='utf-8') as e:
    json.dump(words_list, e)
