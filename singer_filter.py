def raw_filter():
    new_file = open('new_artist.txt', 'w', encoding='utf8')
    filter_file = open('filter_artist.txt', 'w', encoding='utf8')
    f = open('artists.txt', 'r', encoding='utf8').readlines()
    raw = open('raw_hot_singer.txt', 'r', encoding='utf8').readlines()
    for new in raw:
        flag = 0
        for i in f:
            aid, name, tag = i.strip().split('\t')
            if name == new.strip():
                new_file.write(i)
                flag = 1
                break
        if flag == 0:
            filter_file.write(new.strip())
            filter_file.write('\n')

def add_new_artist():
    new = open('new_artist.txt', 'r', encoding='utf8').readlines()
    s = open('s_artist.txt', 'r', encoding='utf8').readlines()
    for n in new:
        x = n.split('\t')[0] + '\t' + n.split('\t')[1] + '\n'
        if x not in s:
            print(x[:-1])
            #s.write(x)

add_new_artist()



