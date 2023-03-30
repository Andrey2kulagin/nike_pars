file = open("all_links_with_duplicate.txt", 'r')
file2 = open('links.txt', "w")
for line in set(file.readlines()):
    file2.write(line)
