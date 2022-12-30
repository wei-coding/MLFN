import urllib
import url_features as urlfe
import pandas as pd
import requests
import tldextract
import re

from urllib.parse import urlparse

def is_URL_accessible(url):
    #iurl = url
    #parsed = urlparse(url)
    #url = parsed.scheme+'://'+parsed.netloc
    page = None
    try:
        page = requests.get(url, timeout=5)   
    except:
        parsed = urlparse(url)
        url = parsed.scheme+'://'+parsed.netloc
        if not parsed.netloc.startswith('www'):
            url = parsed.scheme+'://www.'+parsed.netloc
            try:
                page = requests.get(url, timeout=5)
            except:
                page = None
                pass

    if page and page.status_code == 200 and page.content not in ["b''", "b' '"]:
        return True, url, page
    else:
        return False, url, None

def get_domain(url):
    o = urllib.parse.urlsplit(url)
    return o.hostname, tldextract.extract(url).domain, o.path


def extract_features(url: str) -> pd.DataFrame:

    def words_raw_extraction(domain, subdomain, path):
        w_domain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", domain.lower())
        w_subdomain = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", subdomain.lower())   
        w_path = re.split("\-|\.|\/|\?|\=|\@|\&|\%|\:|\_", path.lower())
        raw_words = w_domain + w_path + w_subdomain
        w_host = w_domain + w_subdomain
        raw_words = list(filter(None,raw_words))
        return raw_words, list(filter(None,w_host)), list(filter(None,w_path))

    status, url, page = is_URL_accessible(url)

    if not status:
        print("can't load in the page, result may have errors.")

    hostname, domain, path = get_domain(url)
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain+'.'+extracted_domain.suffix
    subdomain = extracted_domain.subdomain
    tmp = url[url.find(extracted_domain.suffix):len(url)]
    pth = tmp.partition("/")
    path = pth[1] + pth[2]
    words_raw, words_raw_host, words_raw_path = words_raw_extraction(extracted_domain.domain, subdomain, pth[2])
    tld = extracted_domain.suffix
    parsed = urlparse(url)
    scheme = parsed.scheme
    
    selected_features = ['length_url', 'length_hostname', 'nb_dots', 'nb_hyphens',
    'nb_slash', 'nb_www', 'https_token', 'ratio_digits_url',
    'ratio_digits_host', 'nb_redirection', 'length_words_raw',
    'longest_word_path', 'avg_words_raw', 'avg_word_host',
    'avg_word_path', 'phish_hints', 'domain_in_brand']

    # parse url to features
    row = [
        urlfe.url_length(url),
        urlfe.url_length(hostname),
        urlfe.count_dots(url),
        urlfe.count_hyphens(url),
        urlfe.count_slash(url),
        urlfe.check_www(words_raw),
        urlfe.https_token(scheme),
        urlfe.ratio_digits(url),
        urlfe.ratio_digits(hostname),
        urlfe.count_redirection(page),
        urlfe.length_word_raw(words_raw),
        urlfe.longest_word_length(words_raw_path),
        urlfe.average_word_length(words_raw),
        urlfe.average_word_length(words_raw_host),
        urlfe.average_word_length(words_raw_path),
        urlfe.phish_hints(url),
        urlfe.domain_in_brand(extracted_domain.domain)
    ]

    # create dataframe
    df = pd.DataFrame(columns=selected_features, index=[0])
    df.iloc[0] = row
    
    return df


if __name__ == '__main__':
    extract_features('http://shadetreetechnology.com/V4/validation/a111aedc8ae390eabcfa130e041a10a4')