from html.parser import HTMLParser

# create a subclass and override the handler methods
class NoteParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print ("Encountered a start tag:", tag)
        if (tag "a"):
            print(attrs)

    def handle_endtag(self, tag):
        print ("Encountered an end tag :", tag)

    def handle_data(self, data):
        print ("Encountered some data  :", data)
