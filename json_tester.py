import json


def transfer(input, output):
    f = open(input, 'r')
    data = json.load(f)
    f.close()
    f2 = open(output, 'w', encoding='utf8')
    json.dump(data, f2, ensure_ascii=False, indent=4)
    f2.close()
    f3 = open(output, 'r', encoding='utf8')
    data3 = json.load(f3)
    f3.close()
    print('Success' if data == data3 else 'Error')


if __name__ == '__main__':
    transfer('lyric1.json', 'lyric_part1.json')