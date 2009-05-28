class CONST(object) :
    URI_LOGIN = 'https://www.google.com/accounts/ClientLogin'
    URI_PREFIXE_READER = 'http://www.google.com/reader/'
    URI_PREFIXE_ATOM = URI_PREFIXE_READER + 'atom/'
    URI_PREFIXE_API = URI_PREFIXE_READER + 'api/0/'
    URI_PREFIXE_VIEW = URI_PREFIXE_READER + 'view/'

    ATOM_GET_FEED = 'feed/'

    ATOM_PREFIXE_USER = 'user/-/'
    ATOM_PREFIXE_USER_NUMBER = 'user/'+'0'*20+'/'
    ATOM_PREFIXE_LABEL = ATOM_PREFIXE_USER + 'label/'
    ATOM_PREFIXE_STATE_GOOGLE = ATOM_PREFIXE_USER + 'state/com.google/'

    ATOM_STATE_READ = ATOM_PREFIXE_STATE_GOOGLE + 'read'
    ATOM_STATE_UNREAD = ATOM_PREFIXE_STATE_GOOGLE + 'kept-unread'
    ATOM_STATE_FRESH = ATOM_PREFIXE_STATE_GOOGLE + 'fresh'
    ATOM_STATE_READING_LIST = ATOM_PREFIXE_STATE_GOOGLE + 'reading-list'
    ATOM_STATE_BROADCAST = ATOM_PREFIXE_STATE_GOOGLE + 'broadcast'
    ATOM_STATE_STARRED = ATOM_PREFIXE_STATE_GOOGLE + 'starred'
    ATOM_SUBSCRIPTIONS = ATOM_PREFIXE_STATE_GOOGLE + 'subscriptions'

    API_EDIT_SUBSCRIPTION = 'subscription/edit'
    API_EDIT_TAG = 'edit-tag'

    API_LIST_PREFERENCE = 'preference/list'
    API_LIST_SUBSCRIPTION = 'subscription/list'
    API_LIST_TAG = 'tag/list'
    API_LIST_UNREAD_COUNT = 'unread-count'
    API_TOKEN = 'token'

    URI_QUICKADD = URI_PREFIXE_READER + 'quickadd'

    OUTPUT_XML = 'xml'
    OUTPUT_JSON = 'json'

    AGENT='python-googlereader-contact:pyrfeed-at-gmail/0.1'

    ATOM_ARGS = {
        'start_time' : 'ot',
        'order' : 'r',
        'exclude_target' : 'xt',
        'count' : 'n',
        'continuation' : 'c',
        'client' : 'client',
        'timestamp' : 'ck',
        }

    EDIT_TAG_ARGS = {
        'feed' : 's',
        'entry' : 'i',
        'add' : 'a',
        'remove' : 'r',
        'action' : 'ac',
        'token' : 'T',
        }

    EDIT_SUBSCRIPTION_ARGS = {
        'feed' : 's',
        'entry' : 'i',
        'title' : 't',
        'add' : 'a',
        'remove' : 'r',
        'action' : 'ac',
        'token' : 'T',
        }

    LIST_ARGS = {
        'output' : 'output',
        'client' : 'client',
        'timestamp' : 'ck',
        'all' : 'all'
        }

    QUICKADD_ARGS = {
        'url' : 'quickadd',
        'token' : 'T',
    }

    ORDER_REVERSE = 'o'
    ACTION_REVERSE = 'o'

    GOOGLE_SCHEME = 'http://www.google.com/reader/'

