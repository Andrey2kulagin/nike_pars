file = open("links1_with_duplicate.txt", 'r')
file2 = open('links1.txt', "a")
for line in set(file.readlines()):
    file2.write(line)
