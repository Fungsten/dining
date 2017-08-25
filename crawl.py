import sys
from filters import filter_urls, filter_emails, filter_phones
import requests

class WebPage:

    def __init__(self, url):
        """
        Initializes a WebPage's state with the url, and populates:
        - the set of urls in the WebPages's source
        - the set of emails in the WebPages's source
        - the set of phone numbers in the WebPages's source
        Args:
            url (str): the url to search
        """
        self._url = url
        self._url_set = set()
        self._emails = set()
        self._numbers = set()
        self.text = ""


    def __hash__(self):
        """Return the hash of the URL"""
        return hash(self.url())

    def __eq__(self, page):
        """
        return True if and only if the url of this page equals the url
        of page.
        Args:
            page (WebPage): a WebPage object to compare
        """
        return self._url == page.url

    def populate(self):
        """
        fetch this WebPage object's webpage text and populate its content
        """

        r = requests.get(self._url)
        self.text = self.text + str(r.text)
        if r.status_code == requests.codes.ok:
            for url in filter_urls(r.text):
                self._url_set.add(url)
            for email in filter_emails(r.text):
                self._emails.add(email)
            for number in filter_phones(r.text):
                self._numbers.add(number)

    def rawtext(self):
        """return the everything"""

        return text

    def url(self):
        """return the url asssociated with the WebPage"""

        return self._url

    def phone_numbers(self):
        """return the phone numbers associated with the WebPage"""

        return self._numbers

    def emails(self):
        """return the email addresses associated with the WebPage"""

        return self._emails

    def urls(self):
        """return the URLs associated with the WebPage"""

        return self._url_set



class WebCrawler:
    def __init__(self, base_url, max_links=50):
        """
        Initialize the data structures required to crawl the web.
        Args:
           base_url (str): the starting point of our crawl
           max_links (int): after traversing this many links, stop the crawl
        """
        self.base_url = base_url
        self.max_links = max_links
        self.visited_urls = set()
        self._emails = set()
        self._numbers = set()
        self._rawtext = ""


    def crawl(self):
        """
        starting from self._base_url and until stopping conditions are met,
        creates WebPage objects and recursively explores their links.
        """
        url_list = [self.base_url]
        while len(self.visited_urls) < self.max_links:
            if len(url_list) > 0:
                w = WebPage(url_list.pop(0))
                w.populate()
                url_list = url_list + list(w.urls())
                print(w.url())
                if w.url() not in self.visited_urls:
                    self.visited_urls.add(w.url())
                    print(len(self.visited_urls))
                    self._emails |= w._emails
                    self._numbers |= w._numbers
                    self._rawtext = self._rawtext + w.text

                #self.visited_urls.add(w.url())
                #print(len(self.visited_urls))
                #self._emails |= w._emails
                #self._numbers |= w._numbers
                #self._rawtext = self._rawtext + w.text


    def all_emails(self):
        """
        returns the set of all email addresses harvested during a
        successful crawl
        """

        return self._emails

    def all_phones(self):
        """
        returns the set of all phone numbers harvested during a
        successful crawl
        """

        return self._numbers

    def all_urls(self):
        """
        returns the set of all urls traversed during a crawl
        """

        return self.visited_urls

    def output_results(self, filename):
        """
        In an easy-to-read format, writes the report of a successful crawl
        to the file specified by 'filename'.
        This includes the starting url, the set of urls traversed,
        all emails encountered, and the set of phone numbers (recorded in
        a standardized format of NPA-NXX-XXXX).
        """

        with open(filename, 'w') as f:
            f.write('Crawl starting from {} and crawling a maximum of {} links'.format(self.base_url, self.max_links))
            f.write('\n')
            f.write('\nURLs:\n')
            for url in self.all_urls():
                f.write(url + '\n')
            f.write('\nEmails:\n')
            for email in self.all_emails():
                f.write(email + '\n')
            f.write('\nPhone Numbers:\n')
            for number in self.all_phones():
                f.write(number + '\n')
            f.write(self._rawtext)

def usage():
    print("python3 crawl.py <base_url> <report_file>")
    print("\tbase_url: the initial url to crawl")
    print("\treport_file: file where all results are written")

if __name__ == '__main__':

    #if len(sys.argv) < 3:
    #    usage()
    #    sys.exit(1)

    base_url = "https://dining.williams.edu/eats4ephs/?unitid=27&meal=BREAKFAST"
    report_path = "text.json"

    crawl = WebCrawler(base_url, max_links=1) # until you are confident use small max_links
    crawl.crawl()
    crawl.output_results(report_path)
