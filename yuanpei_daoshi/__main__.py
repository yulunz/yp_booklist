import json

from yuanpei_daoshi.crawl import crawl_all


def main():
    daoshi = crawl_all()
    with open('daoshi.json', 'w', encoding='utf-8') as f:
        json.dump(daoshi, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()

