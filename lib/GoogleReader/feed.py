import time
from xml.dom import minidom

# TODO : Use those line when python 2.6 will be out, for now, there is no
#        reasons to not be compatible with python 2.4 just to please PEP 238 !
#        (lines will be mandatory only with python 2.7)
# from .const import CONST
from const import CONST


class GoogleFeed(object) :
    def __init__(self,xmlfeed) :
        # Need a lot more check !!!
        self._document = minidom.parseString(xmlfeed)
        self._entries = []
        self._properties = {}
        self._continuation = None
        self._isotime_pos = [(0,4),(5,7),(8,10),(11,13),(14,16),(17,19)]
        for feedelements in self._document.childNodes[0].childNodes :
            if feedelements.localName == 'entry' :
                self._entries.append(feedelements)
            elif feedelements.localName == 'continuation' :
                self._continuation = feedelements.firstChild.data
            else :
                self._properties[feedelements.localName] = feedelements
    def get_title(self) :
        if 'title' in self._properties :
            return self._properties['title'].childNodes[0].data
    def get_entries(self) :
        for dom_entry in self._entries :
            entry = {}
            entry['categories'] = {}
            entry['sources'] = {}
            entry['crawled'] = int(dom_entry.getAttribute('gr:crawl-timestamp-msec'))
            for dom_entry_element in dom_entry.childNodes :
                if dom_entry_element.localName == 'id' :
                    entry['google_id'] = dom_entry_element.firstChild.data
                    entry['original_id'] = dom_entry_element.getAttribute('gr:original-id')
                elif dom_entry_element.localName == 'link' :
                    if dom_entry_element.getAttribute('rel')=='alternate' :
                        entry['link'] = dom_entry_element.getAttribute('href')
                elif dom_entry_element.localName == 'category' :
                    if dom_entry_element.getAttribute('scheme')==CONST.GOOGLE_SCHEME :
                        term = dom_entry_element.getAttribute('term')
                        digit_table = {
                            ord('0'):ord('0'),
                            ord('1'):ord('0'),
                            ord('2'):ord('0'),
                            ord('3'):ord('0'),
                            ord('4'):ord('0'),
                            ord('5'):ord('0'),
                            ord('6'):ord('0'),
                            ord('7'):ord('0'),
                            ord('8'):ord('0'),
                            ord('9'):ord('0'),
                            }
                        if term.translate(digit_table).startswith(CONST.ATOM_PREFIXE_USER_NUMBER) :
                            term = CONST.ATOM_PREFIXE_USER + term[len(CONST.ATOM_PREFIXE_USER_NUMBER):]
                        entry['categories'][term] = dom_entry_element.getAttribute('label')
                elif dom_entry_element.localName == 'summary' :
                    entry['summary'] = dom_entry_element.firstChild.data
                elif dom_entry_element.localName == 'content' :
                    entry['content'] = dom_entry_element.firstChild.data
                elif dom_entry_element.localName == 'author' :
                    entry['author'] = dom_entry_element.getElementsByTagName('name')[0].firstChild.data
                elif dom_entry_element.localName == 'title' :
                    entry['title'] = dom_entry_element.firstChild.data
                elif dom_entry_element.localName == 'source' :
                    entry['sources'][dom_entry_element.getAttribute('gr:stream-id')] = dom_entry_element.getElementsByTagName('id')[0].firstChild.data
                elif dom_entry_element.localName == 'published' :
                    entry['published'] = self.iso2time(dom_entry_element.firstChild.data)
                elif dom_entry_element.localName == 'updated' :
                    entry['updated'] = self.iso2time(dom_entry_element.firstChild.data)
            for entry_key in ('link','summary','author','title') :
                if entry_key not in entry :
                    entry[entry_key] = u''
            for entry_key in ('published','updated','crawled') :
                if entry_key not in entry :
                    entry[entry_key] = None
            if 'content' not in entry :
                entry['content'] = entry['summary']
            yield entry
    def get_continuation(self) :
        return self._continuation
    def iso2time(self,isodate) :
        # Ok, it's unreadable ! So, I have z == '2006-12-17T12:07:19Z',
        # I take z[0:4] and z[5:7] and etc.,
        # ('2006','12', etc.)
        # I convert them into int, And I add [0,0,0]
        # Once converted in tuple, I got (2006,12,17,12,07,19,0,0,0), which is what mktime want...
        return time.mktime(tuple(map(lambda x:int(isodate.__getslice__(*x)),self._isotime_pos)+[0,0,0]))

