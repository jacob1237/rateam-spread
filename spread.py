#!/usr/bin/env python3

import sys
import random
from urllib.request import urlopen, Request
from lxml.html import parse


URL_NONCASH = 'https://rate.am/en/armenian-dram-exchange-rates/banks/non-cash'
URL_CASH = 'https://rate.am/en/armenian-dram-exchange-rates/banks/cash'

XPATH_BUY_RATES_NONCASH = '//table[@id="rb"]//tr[@id]/td[2]/a/text()|//table[@id="rb"]//tr[@id]/td[6]//text()'
XPATH_SELL_RATES_CASH = '//table[@id="rb"]//tr[@id]/td[2]/a/text()|//table[@id="rb"]//tr[@id]/td[7]//text()'

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)',
]


def parse_table(url, query, user_agent=None):
    user_agent = user_agent or random.choice(USER_AGENTS)

    req = Request(url, headers={'User-Agent' : user_agent})
    data = parse(urlopen(req)).xpath(query)

    return dict(zip(data[::2], data[1::2]))


def err(msg, code=1):
    sys.stderr.write(msg)
    return code


def main():
    if len(sys.argv) <= 1:
        return err('Please provide a bank name\n')

    buy = parse_table(URL_NONCASH, XPATH_BUY_RATES_NONCASH)

    target_bank = sys.argv[1]
    bank_names = buy.keys()
    rate = float(buy[target_bank])

    if target_bank not in bank_names:
        return err('Invalid bank name: "{0}"\n\nChoose from the following:\n  {1}\n'.format(target_bank, '\n  '.join(sorted(bank_names))))

    sell = parse_table(URL_CASH, XPATH_SELL_RATES_CASH)

    print('Best USD spread\n---------------')

    for name in sorted(sell, key=sell.get)[0:5]:
        price = float(sell[name])
        print('{0}: {1:.3f}%'.format(name.strip(), (1.0 - rate/price) * 100))

    return 0


if __name__ == '__main__':
    sys.exit(main())

