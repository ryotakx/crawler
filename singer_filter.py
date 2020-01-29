
new_file = open('new_artist.txt', 'w', encoding='utf8')
filter_file = open('filter_artist.txt', 'w', encoding='utf8')
f = open('artists.txt', 'r', encoding='utf8').readlines()
for line in open('raw_hot_singer.txt', 'r', encoding='utf8').readlines():
    for i in f:
        print(i, line)
        aid, name, tag = i.strip().split('\t')
        if line.strip() == name:
            new_file.write(i)
            break
    filter_file.write(line.strip())
    filter_file.write('\n')


