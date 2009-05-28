# TODO : Use those line when python 2.6 will be out, for now, there is no
#        reasons to not be compatible with python 2.4 just to please PEP 238 !
#        (lines will be mandatory only with python 2.7)
# from .const import CONST
from const import CONST

from xml.dom import minidom

class GoogleObject(object) :
    """ This class aims at reading 'object' xml structure.
        Look like it's based on something jsoinsable.
        ( http://json.org/ )
        Yes I'm a moron ( in the sense defined by the asshole/moron spec
        http://www.diveintomark.org/archives/2004/08/16/specs ),
        which means everything is just supposition.

        A json can contains only string, number, object, array, true,
        false, null.

        It look like Google Reader use string for true and false.
        Never seen 'null' neither.

        A GoogleObject can only contains string, number, object, array
        """
    def __init__(self,xmlobject) :
        """ 'xmlobject' is the string containing the answer from Google as
            an object jsonizable. """
        self._document = minidom.parseString(xmlobject)
    def parse(self) :
        """ 'parse' parse the object and return the pythonic version of
            the object. """
        return self._parse_dom_element(self._document.childNodes[0])
    def _parse_dom_element(self,dom_element) :
        value = None
        if dom_element.localName == 'object' :
            value = {}
            for childNode in dom_element.childNodes :
                if childNode.localName != None :
                    name = childNode.getAttribute('name')
                    value[name] = self._parse_dom_element(childNode)
        elif dom_element.localName == 'list' :
            value = []
            for childNode in dom_element.childNodes :
                if childNode.localName != None :
                    value.append(self._parse_dom_element(childNode))
        elif dom_element.localName == 'number' :
            value = int(dom_element.firstChild.data)
        elif dom_element.localName == 'string' :
            value = dom_element.firstChild.data
        # let's act as a total moron : Never seen those balise, but
        # I can imagine them may exist by reading http://json.org/
        elif dom_element.localName == 'true' :
            value = True
        elif dom_element.localName == 'false' :
            value = False
        elif dom_element.localName == 'null' :
            value = None
        return value

