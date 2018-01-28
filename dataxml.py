import zipfile
import re



from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")
(options, args) = parser.parse_args()
#print options.filename

# Which file are we working with?
fname = options.filename

#print fname


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s

def get_epub_info(fname):


    # prepare to read from the .epub file
    epubZip = zipfile.ZipFile(fname)

    txt = epubZip.read('META-INF/container.xml')
    #txt1 = epubZip.read('content.opf')

    #print txt
    result = re.findall('(?<=full-path=").*?(?=" )', txt)
    #print result[0]
    #print txt1
    # find the contents metafile
    resume =epubZip.read(result[0])

    #print resume
    description = re.findall("(?s)(?<=<dc:description>).*(?=</dc:description>)", resume)
    #description== html_decode(description)
    #print description[0]
    try:
        gotdata = description[0]
    except IndexError:
        description = ['Pas de description']
    resume=  html_decode(description[0])
    print remove_html_markup(resume)

    #file = open("testfile.txt","w")
    file = open("testfile.txt","a")

    file.write(remove_html_markup(resume).replace('\n', ''))


    file.close()

    return ""

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

#print get_epub_info("jean2.epub")
print get_epub_info(fname)