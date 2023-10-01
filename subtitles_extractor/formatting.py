import srt
from bs4 import BeautifulSoup


def strip(data):
    subs = tuple(srt.parse(data))

    for sub in subs:
        sub.content = BeautifulSoup(sub.content, "html.parser").text

    return srt.compose(subs)
