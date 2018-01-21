import urllib2
import os
from bs4 import BeautifulSoup as BS

# Set to see intermediate outputs.
DEBUG = False

Directory = 'Articles'
Publishers = {
    'scroll': 'https://scroll.in/category/76/politics/page/',
}


def scroll():
    ''' Gets list of news articles from scroll,
    and saves them under folder ./scroll. '''

    # NewsLinks contains news links to articles.
    NewsLinks = []
    # Number of pages to crawl.
    pages = 10
    for page in xrange(1, pages):
        html = urllib2.urlopen(Publishers['scroll'] + str(page))
        soup = BS(html, 'html.parser')

        children = soup.find_all('li', class_='row-story')
        for child in children:
            news = (child.find('h1').text,)
            news += (child.find('link').attrs['href'],)
            news += (child.find('time').attrs['datetime'],)
            news += (child.find('img').attrs['src'],)
            NewsLinks.append(news)

    if DEBUG:
        print NewsLinks

    # For numbering articles being saved.
    file_counter = 1

    # Iterate over links of NewsLinks list, and save the content to files.
    for title, link, timestamp, imageurl in NewsLinks:
        html = urllib2.urlopen(link)
        soup = BS(html, 'html.parser')
        # Nested list with article contents in between.
        news_chunks = soup.find('div', class_='article-body').find_all('p')
        news_complete = ' '.join([chunk.text for chunk in news_chunks])

        if DEBUG:
            print title
            print news_complete

        # Save all non-empty the article.
        if len(news_complete.strip()):

            filename = os.path.join(
                Directory, 'scroll_' + str(file_counter) + '.txt')
            imgpath = os.path.join(
                Directory, 'scroll_' + str(file_counter) + '.jpg')
            fp = open(filename, 'w')
            fp.write((title + '\n' + timestamp + '\n\n' +
                      news_complete + '\n').encode("utf-8"))
            fp.close()

            img_obj = urllib2.urlopen(imageurl)
            img_file = open(imgpath, 'wb')
            img_file.write(img_obj.read())
            img_file.close()

            print "Article #", file_counter, ':', title
            file_counter += 1


def main():
    for publisher in Publishers:
        if publisher == 'scroll':
            scroll()


if __name__ == '__main__':
    if not os.path.exists(Directory):
        os.makedirs(Directory)
    main()
