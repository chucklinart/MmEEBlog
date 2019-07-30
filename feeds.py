from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.contrib.sites.models import Site
from django.urls import reverse
from mmeeblog.models import Blog

# a lot of CHANGEMEs in here
class RssFeed(Feed):
    title = "Chuck Linart Feed"
    link = "/blog/"
    author_name = "Chuck Linart"
    author_email = "nobody@nowhere.com"
    author_link = "https://chucklinart.com"
    categories = ["News &amp; Politics, Tech, Music, Philosophy"]
    feed_copyright = "Creative Commons Attribution 4.0 International"
    description = "Chuck Linart is a pretty cool dude who has fresh " +\
                  "ideas about tech, news, music and life in general. " +\
                  "He is funny and DGAF while blowing your mind " +\
                  "about whatever is on his."

    def items(self):
        return Blog.objects.order_by('-posted').all()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return "https://chucklinart.com/" + item.slug

    def item_author_name(self, item):
        return "{} {}".format(item.creator.user.first_name, item.creator.user.last_name)

    def item_pubdate(self, item):
        return item.posted

class AtomFeed(Feed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description

class iTunesFeed(Rss201rev2Feed):
    def rss_attributes(self):
        return {
            "version": self._version,
            "xmlns:atom": "http://www.w3.org/2005/Atom",
            'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'
        }

    def add_root_elements(self, handler):
        super().add_root_elements(handler)
        handler.addQuickElement('itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement('itunes:author', self.feed['author_name'])
        handler.addQuickElement('itunes:summary', self.feed['description'])
        handler.addQuickElement('itunes:category',
                                self.feed['iTunes_category'])
        handler.addQuickElement('itunes:explicit',
                                self.feed['iTunes_explicit'])
        handler.startElement("itunes:owner", {})
        handler.addQuickElement('itunes:name', self.feed['iTunes_name'])
        handler.addQuickElement('itunes:email', self.feed['iTunes_email'])
        handler.endElement("itunes:owner")
        handler.addQuickElement('itunes:image', self.feed['iTunes_image_url'])

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement(u'itunes:summary', item['summary'])
        handler.addQuickElement(u'itunes:duration', item['duration'])
        handler.addQuickElement(u'itunes:explicit', item['explicit'])

# CHANGEMEs below

class AudioFeed(AtomFeed):
    iTunes_explicit = 'explicit'
    iTunes_name = "Chuck Linart"
    iTunes_email = "hello@chucklinart.com"
    iTunes_image_url = "https://chucklinat.com/media/blogimg/2019/03/06/site-profile-nofxweb_yE4D0kc.jpg"
    feed_type = iTunesFeed

    def items(self):
        return Podcast.objects.order_by('-pubdate').all()

    def feed_extra_kwargs(self, obj):
        return {
            'iTunes_name': self.iTunes_name,
            'iTunes_email': self.iTunes_email,
            'iTunes_image_url': self.iTunes_image_url,
            'iTunes_explicit': self.iTunes_explicit,
            'iTunes_category': 'News &amp; Politics'
        }

    def item_extra_kwargs(self, item):
        return {
            'summary': item.summary,
            'duration': item.duration,
            'explicit': 'explicit' if item.explicit else 'no',
        }

    def item_enclosure_url(self, item):
        return "https://chucklinart.com/" + str(item.filepath)

    def item_enclosure_length(self, item):
        return item.duration

    def item_enclosure_mime_type(self, item):
        return 'audio/mp3'
