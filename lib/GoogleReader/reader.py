import time
import urllib
import cookielib
# TODO : Get rise of web package.
from web import web

# TODO : Use those line when python 2.6 will be out, for now, there is no
#        reasons to not be compatible with python 2.4 just to please PEP 238 !
#        (lines will be mandatory only with python 2.7)
# from .feed import GoogleFeed
# from .object import GoogleObject
# from .const import CONST
from feed import GoogleFeed
from object import GoogleObject
from const import CONST

class GoogleReader(object) :
    def __init__(self,agent=None,http_proxy=None) :
        self._login = None
        self._passwd = None

        self._agent = agent or CONST.AGENT
        self._web = web(agent=self._agent,http_proxy=http_proxy)
        self._sid = None

        self._token = None

    # ---------------------------------------------------------------
    # Login process
    # ---------------------------------------------------------------

    def identify(self,login,passwd) :
        ''' Provide login and passwd to the GoogleReader object. You must call this before login.'''
        self._login = login
        self._passwd = passwd

    def login(self) :
        ''' Login into GoogleReader. You must call identify before calling this.
            You must call this before anything else that acces to GoogleReader data.'''
        if self._login==None or self._passwd == None :
            return


        data = {
            'service':'reader',
            'Email':self._login,
            'Passwd':self._passwd,
            'source':CONST.AGENT,
            'continue':'http://www.google.com/',
            }

        sidinfo = self._web.get( CONST.URI_LOGIN, data )
        # print sidinfo

        self._sid = None
        SID_ID = 'SID='
        if SID_ID in sidinfo :
            pos_beg = sidinfo.find(SID_ID)
            pos_end = sidinfo.find('\n',pos_beg)
            self._sid = sidinfo[pos_beg+len(SID_ID):pos_end]
        if self._sid != None :
            cookie = cookielib.Cookie(version=0, name='SID', value=self._sid, port=None, port_specified=False, domain='.google.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires='1600000000', discard=False, comment=None, comment_url=None, rest={})
            self._web.cookies().set_cookie(cookie)

            return True

    # ---------------------------------------------------------------
    # Very low
    # ---------------------------------------------------------------

    def get_token(self,force=False) :
        if ( force or (self._token == None) ) :
            feedurl = CONST.URI_PREFIXE_API + CONST.API_TOKEN + '?client=' + CONST.AGENT
            # print feedurl
            self._token = self._web.get(feedurl)
        return self._token

    def get_timestamp(self) :
        return str(int(1000*time.time()))

    def _translate_args(self, dictionary, googleargs, kwargs) :
        """ _translate_args takes a 'dictionary' to translate argument names
            in 'kwargs' from this API to google names.
            It also serve as a filter.
            Nothing is returned 'googleargs' is just updated.
            """
        for arg in dictionary :
            if arg in kwargs :
                googleargs[dictionary[arg]] = kwargs[arg]
            if dictionary[arg] in kwargs :
                googleargs[dictionary[arg]] = kwargs[dictionary[arg]]

    # ---------------------------------------------------------------
    # Low
    # ---------------------------------------------------------------

    def get_feed(self,url=None,feed=None,**kwargs) :
        """ 'get_feed' returns a GoogleFeed, giving either an 'url' or a 'feed' internal name.
            other arguments may be any keys of CONST.ATOM_ARGS keys
            """
        if url != None :
            feed = CONST.ATOM_GET_FEED + urllib.quote_plus(url)
        if feed == None :
            feed = CONST.ATOM_STATE_READING_LIST
        feedurl = CONST.URI_PREFIXE_ATOM + feed
        urlargs = {}
        kwargs['client'] = CONST.AGENT
        kwargs['timestamp'] = self.get_timestamp()
        self._translate_args( CONST.ATOM_ARGS, urlargs, kwargs )

        atomfeed = self._web.get(feedurl + '?' + urllib.urlencode(urlargs))
        if atomfeed != '' :
            return GoogleFeed(atomfeed)

        return None

    def get_api_list(self,apiurl,**kwargs) :
        """ 'get_api_list' returns a structure than can be send either
            by json or xml, I used xml because... I felt like it.
            """
        urlargs = {}
        kwargs['output'] = CONST.OUTPUT_XML
        kwargs['client'] = CONST.AGENT
        kwargs['timestamp'] = self.get_timestamp()
        self._translate_args( CONST.LIST_ARGS, urlargs, kwargs )
        xmlobject = self._web.get(apiurl + '?' + urllib.urlencode(urlargs))
        if xmlobject != '' :
            return GoogleObject(xmlobject).parse()
        return None

    def edit_api( self, target_edit, dict_args, **kwargs ) :
        """ 'edit_api' wrap Google Reader API for editting database.
            """
        urlargs = {}
        urlargs['client'] = CONST.AGENT

        postargs = {}
        kwargs['token'] = self.get_token()
        self._translate_args( dict_args, postargs, kwargs )

        feedurl = CONST.URI_PREFIXE_API + target_edit + '?' + urllib.urlencode(urlargs)
        result_edit = self._web.post(feedurl,postargs)
        # print "result_edit:[%s]"%result_edit
        if result_edit != 'OK' :
            # just change the token and try one more time !
            kwargs['token'] = self.get_token(force=True)
            self._translate_args( dict_args, postargs, kwargs )
            result_edit = self._web.post(feedurl,postargs)
            # print "result_edit_bis:[%s]"%result_edit
        return result_edit

    # ---------------------------------------------------------------
    # Middle
    # ---------------------------------------------------------------

    def edit_tag( self, **kwargs ) :
        if 'feed' not in kwargs :
            kwargs['feed'] = CONST.ATOM_STATE_READING_LIST
        kwargs['action'] = 'edit-tags'

        return self.edit_api( CONST.API_EDIT_TAG, CONST.EDIT_TAG_ARGS, **kwargs )

    def edit_subscription( self, **kwargs ) :
        if 'action' not in kwargs :
            kwargs['action'] = 'edit'
        if 'item' not in kwargs :
            kwargs['item'] = 'null'
        return self.edit_api( CONST.API_EDIT_SUBSCRIPTION, CONST.EDIT_SUBSCRIPTION_ARGS, **kwargs )

    def get_preference(self) :
        """ 'get_preference' returns a structure containing preferences.
            """
        return self.get_api_list(CONST.URI_PREFIXE_API + CONST.API_LIST_PREFERENCE)

    def get_subscription_list(self) :
        """ 'get_subscription_list' returns a structure containing subscriptions.
            """
        return self.get_api_list(CONST.URI_PREFIXE_API + CONST.API_LIST_SUBSCRIPTION)

    def get_tag_list(self) :
        """ 'get_tag_list' returns a structure containing tags.
            """
        return self.get_api_list(CONST.URI_PREFIXE_API + CONST.API_LIST_TAG)

    def get_unread_count_list(self) :
        """ 'get_unread_count_list' returns a structure containing the number
            of unread items in each subscriptions/tags.
            """
        return self.get_api_list(CONST.URI_PREFIXE_API + CONST.API_LIST_UNREAD_COUNT, all='true')

    # ---------------------------------------------------------------
    # High
    # ---------------------------------------------------------------

    def get_all(self) :
        return self.get_feed()

    def get_unread(self) :
        return self.get_feed( exclude_target=CONST.ATOM_STATE_READ )

    def set_read(self,entry) :
        self.edit_tag( entry=entry, add=CONST.ATOM_STATE_READ, remove=CONST.ATOM_STATE_UNREAD )

    def set_unread(self,entry) :
        self.edit_tag( entry=entry, add=CONST.ATOM_STATE_UNREAD, remove=CONST.ATOM_STATE_READ )

    def add_star(self,entry) :
        self.edit_tag( entry=entry, add=CONST.ATOM_STATE_STARRED )

    def del_star(self,entry) :
        self.edit_tag( entry=entry, remove=CONST.ATOM_STATE_STARRED )

    def add_public(self,entry) :
        self.edit_tag( entry=entry, add=CONST.ATOM_STATE_BROADCAST )

    def del_public(self,entry) :
        self.edit_tag( entry=entry, remove=CONST.ATOM_STATE_BROADCAST )

    def add_label(self,entry,labelname) :
        self.edit_tag( entry=entry, add=CONST.ATOM_PREFIXE_LABEL+labelname )

    def del_label(self,entry,labelname) :
        self.edit_tag( entry=entry, remove=CONST.ATOM_PREFIXE_LABEL+labelname )

    def add_subscription(self,url=None,feed=None,labels=[],**kwargs) :
        postargs = {}
        result_edit = None
        if (feed is not None) or (url is not None) :
            if feed is None :
                kwargs['url'] = url
                kwargs['token'] = self.get_token(force=True)
                self._translate_args( CONST.QUICKADD_ARGS, postargs, kwargs )
                result_edit = self._web.post(CONST.URI_QUICKADD,postargs)
                # print "result_edit:[%s]"%result_edit
                if "QuickAdd_success('" in result_edit :
                    start_pos = result_edit.find("QuickAdd_success('")
                    stop_pos = result_edit.rfind("')")
                    uri_orig, feed = result_edit[start_pos+len("QuickAdd_success('"):stop_pos].split("','")
            else :
                result_edit = self.edit_subscription(feed=feed,action='subscribe')
            for label in labels :
                # print feed,CONST.ATOM_PREFIXE_LABEL+label
                self.edit_subscription(feed=feed,add=CONST.ATOM_PREFIXE_LABEL+label.lower())
        return result_edit

    def del_subscription(self,feed,**kwargs) :
        postargs = {}
        result_edit = None
        if feed is not None :
            result_edit = self.edit_subscription(feed=feed,action='unsubscribe')
        return result_edit

def test() :
    from private import login_info

    gr = GoogleReader()
    gr.identify(**login_info)
    if gr.login():
        print "Login OK"
    else :
        print "Login KO"
        return
    #print "[%s]" % gr.get_token()

    # print gr.set_read("tag:google.com,2005:reader/item/c3abf620979a5d06")
    # print gr.set_unread("tag:google.com,2005:reader/item/8b1030db93c70e9e")
    # print gr.del_label(entry="tag:google.com,2005:reader/item/8b1030db93c70e9e",labelname="vorkana")
    # xmlfeed = gr.get_feed(feed=CONST.ATOM_PREFIXE_LABEL+'url',order=CONST.ORDER_REVERSE,start_time=1165482202,count=15)
    # print xmlfeed
    # print xmlfeed.get_title()
    # for entry in xmlfeed.get_entries() :
    #     print "    %s\n"%entry['title']
    #     print "      %s\n"%entry['published']
    # continuation = xmlfeed.get_continuation()
    # print "(%s)\n"%continuation
    #
    # while continuation != None :
    #     xmlfeed = gr.get_feed(feed=CONST.ATOM_PREFIXE_LABEL+'url',order=CONST.ORDER_REVERSE,start_time=1165482202,count=2,continuation=continuation)
    #     print xmlfeed
    #     print xmlfeed.get_title()
    #     for entry in xmlfeed.get_entries() :
    #         print "    %s\n"%entry['title']
    #         print "      %s\n"%entry['published']
    #     continuation = xmlfeed.get_continuation()
    #     print "(%s)\n"%continuation

    # print gr.get_preference()
    # print gr.get_subscription_list()
    # print gr.get_tag_list()


    # print gr.get_feed("http://action.giss.ath.cx/RSSRewriter.py/freenews",order=CONST.ORDER_REVERSE,start_time=1165482202,count=2)

    #gf = GoogleFeed(xmlfeed)
    #print gf.get_title()


    xmlfeed = gr.get_feed(order=CONST.ORDER_REVERSE,count=3,ot=1166607627)
    print xmlfeed.get_title()
    for entry in xmlfeed.get_entries() :
        print "    %s %s %s\n" % (entry['google_id'],entry['published'],entry['title'])
    print xmlfeed.get_continuation()

    xmlfeed = gr.get_feed(order=CONST.ORDER_REVERSE,count=3)
    print xmlfeed.get_title()
    for entry in xmlfeed.get_entries() :
        print "    %s %s %s\n" % (entry['google_id'],entry['published'],entry['title'])
    print xmlfeed.get_continuation()

if __name__=='__main__' :
    test()
