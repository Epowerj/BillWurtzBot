from html.parser import HTMLParser

# create a subclass and override the handler methods
class NoteParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global notelist

        if (tag == "a"):
            notelist.append(attrs['href'])
