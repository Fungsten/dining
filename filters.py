import re


def filter_urls(text, domain='williams.edu'):
    """
    returns a list of urls found in the string 'text' that are
    (1) not media files and (2) within the specified domain.
    Args:
        text (str): a string that represents the text of a webpage
        domain (str): a <sub-domain> + '.' + <top-level domain>
    """
    def extension_is_valid(url):
        EXTS = ["jpg", "jpeg", "svg", "png", "pdf",
                "gif", "bmp", "mp3", "dvi"]
        for e in EXTS:
            if url.casefold().endswith(e):
                return False
        return True

    domain, tld = domain.split(".")
    # '<a' + _not >_ + 'href=' + _quote_ + 'http://' + _nonquote_ + _quote_
    REGEX = r'''<a[^>]+href\s*=\s*["'](http://.+?(?!["']){}\.{}[^"']+?)["']'''
    REGEX = re.compile(REGEX.format(domain, tld))

    urls = re.findall(REGEX, text)
    return [url for url in urls if extension_is_valid(url)]


def filter_emails(text):
    """
    returns a list of emails found in the string 'text'
    """
    def local_is_valid(local_email):
        inval = ['..', '@@']
        for i in inval:
            if i in local_email:
                return False
        return True

    REGEX = '''[\w.!#$%&'*+-/=?^_`{|}~]+@[\w.]+\.[a-z]+'''

    emails = re.findall(REGEX, text)
    return [email for email in emails if local_is_valid(email)]

def filter_phones(text):
    """
    returns a list of uniformly formatted phone numbers extracted from
    the string 'text'
    """

    REGEX = '''[\d]{3}[\W]{0,3}[\d]{3}[\W]{0,3}[\d]{4}'''
    numbers = re.findall(REGEX, text)
    def reformat(phone):
        num = []
        for n in phone:
            j = n.replace(' ','').replace('.','').replace('-','').replace('(','').replace(')','').replace('>','')
            num.append('{}-{}-{}'.format(j[:3], j[3:6], j[6:10]))
        return num

    return reformat(numbers)
