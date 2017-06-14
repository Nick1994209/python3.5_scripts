with open('words.txt') as file_:
    words = list(file_.readlines())

with open('words2.txt', 'w') as file_2:
    for word in words:
        word.replace('\t', ' ')
        try:
            eng, rus = word.split()
            string = eng + '\t' + rus + '\n'
        except:
            string = word

        file_2.write(string)
