#!/usr/bin/env python

import urllib2

def resolvUrl( base, rel ) :
    urlbase = urllib2.urlparse.urlparse(base)
    urlrel = urllib2.urlparse.urlparse(rel)
    urlfinal = ('','','','','','')
    # Let's assume len(urlrel[0])==0 <=> len(urlrel[1])==0
    # (they are both empty or both non empty)

    # Let's ignore 3 !
    if urlrel[1] == '' :
        if urlrel[2]=='' :
            # this is a '?p=1' or a '#anchor' url...
            if urlrel[4]=='' :
                urlfinal = urlbase[0:5] + urlrel[5:6]
            else :
                urlfinal = urlbase[0:4] + urlrel[4:6]
        else :
            if urlrel[2][0] == '/' :
                # The path is absolute, but without server...
                urlfinal = urlbase[0:2] + urlrel[2:6]
            else :
                # The path is relative, without server...
                urlfinal = urlbase[0:2] + ( urllib2.posixpath.join( urllib2.posixpath.dirname(urlbase[2]), urlrel[2] ), ) + urlrel[3:6]
    else :
        # The rel is absolute...
        urlfinal = urlrel

    return urllib2.urlparse.urlunparse(urlfinal)


