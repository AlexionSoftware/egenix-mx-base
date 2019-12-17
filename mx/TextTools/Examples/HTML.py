#!/usr/local/bin/python

""" HTML - tag a HTML string (Version 0.6)
    
    Copyright (c) 2000, Marc-Andre Lemburg; mailto:mal@lemburg.com
    Copyright (c) 2000-2015, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""

import sys

# constants + engine
from mx.TextTools import *

# ErrorTag
error = '*syntax error'                 # error tag obj

tagname_charset = CharSet(alpha+'\-'+number)
tagattrname_charset = CharSet(alpha+'\-'+number)
tagvalue_charset = CharSet('^"\'> ')
white_charset = CharSet(' \r\n\t')

tagname_charset = CharSet(alpha+'\-'+number)
tagattrname_charset = CharSet(alpha+'\-'+number)
tagvalue_charset = CharSet('^"\'> ')
white_charset = CharSet(' \r\n\t')

tagattr = (
       # name
       ('name',AllInCharSet,tagattrname_charset),
       # with value ?
       (None,Is,'=',MatchOk),
       # skip junk
       (None,AllInCharSet,white_charset,+1),
       # unquoted value
       ('value',AllInCharSet,tagvalue_charset,+1,MatchOk),
       # double quoted value
       (None,Is,'"',+5),
         ('value',AllNotIn,'"',+1,+2),
         ('value',Skip,0),
         (None,Is,'"'),
         (None,Jump,To,MatchOk),
       # single quoted value
       (None,Is,'\''),
         ('value',AllNotIn,'\'',+1,+2),
         ('value',Skip,0),
         (None,Is,'\'')
       )

valuetable = (
    # ignore whitespace + '='
    (None,AllInCharSet,CharSet(' \r\n\t='),+1),
    # unquoted value
    ('value',AllInCharSet,tagvalue_charset,+1,MatchOk),
    # double quoted value
    (None,Is,'"',+5),
     ('value',AllNotIn,'"',+1,+2),
     ('value',Skip,0),
     (None,Is,'"'),
     (None,Jump,To,MatchOk),
    # single quoted value
    (None,Is,'\''),
     ('value',AllNotIn,'\'',+1,+2),
     ('value',Skip,0),
     (None,Is,'\'')
    )

allattrs = (
    # look for attributes
    (None,AllInCharSet,white_charset,+4),
     (None,Is,'>',+1,MatchOk),
     ('tagattr',Table,tagattr),
     (None,Jump,To,-3),
    (None,Is,'>',+1,MatchOk),
    # handle incorrect attributes
    (error,AllNotIn,'> \r\n\t'),
    (None,Jump,To,-6)
    )

# NOTE: The htmltag tag table assumes that the input text is given 
#       in upper case letters (see <XMP> handling).

htmltag = (
    (None,Is,'<'),
    # is this a closing tag ?
    ('closetag',Is,'/',+1),
    # a coment ?
    ('comment',Is,'!',+8),
     (None,Word,'--',+4),
     ('text',WordStart,'-->',+1),
     (None,Skip,3),
     (None,Jump,To,MatchOk),
     # a SGML-Tag ?
     ('other',AllNotIn,'>',+1),
      (None,Is,'>'),
     (None,Jump,To,MatchOk),
    # XMP-Tag ?
    ('tagname',Word,'XMP',+5),
     (None,Is,'>'),
     ('text',WordStart,'</XMP>'),
     (None,Skip,len('</XMP>')),
     (None,Jump,To,MatchOk),
    # get the tag name
    ('tagname',AllInCharSet,tagname_charset),
    # look for attributes
    (None,AllInCharSet,white_charset,+4),
     (None,Is,'>',+1,MatchOk),
     ('tagattr',Table,tagattr),
     (None,Jump,To,-3),
     (None,Is,'>',+1,MatchOk),
    # handle incorrect attributes
    (error,AllNotIn,'> \n\r\t'),
    (None,Jump,To,-6)
    )

htmltable = (# HTML-Tag
             ('htmltag',Table,htmltag,+1,+4),
             # not HTML, but still using this syntax: error or inside XMP-tag !
             (error,Is,'<',+3),
              (error,AllNotIn,'>',+1),
              (error,Is,'>'),
             # normal text
             ('text',AllNotIn,'<',+1),
             # end of file
             ('eof',EOF,Here,-5),
            )

if __name__ == '__main__':

    t = TextTools._timer()

    # read file
    f = open(sys.argv[1])
    text = f.read()

    try:
        count = int(sys.argv[2])
    except:
        count = 1000
    
    print 'Starting to parse the file %i times...' % count

    # parse file
    t.start()
    for i in range(count):
        utext = upper(text)
        result, taglist, nextindex = tag(utext,htmltable)
        if not result:
            print ' parsing failed; aborting'
            break
    t = t.stop()[0]

    mean = t/count
    print result, nextindex, mean*1000,'msec',nextindex/mean,'bytes/sec.'
    print
    print 'Hit return to see the tags...'
    raw_input()
    print
    print_tags(text,taglist)
