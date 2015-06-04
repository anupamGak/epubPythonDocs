import zipfile
import re

reAbbr = re.compile("(?<= )[A-Z]")

container_xml = """<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf"
     media-type="application/oebps-package+xml" />
  </rootfiles>
</container>"""

content_opf = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/" unique-identifier="bookid" version="2.0">
  <metadata>
    <dc:title>%s</dc:title>
    <dc:creator>Python  Documentation</dc:creator>
    <dc:identifier id="bookid">urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658</dc:identifier>
    <dc:language>en-US</dc:language>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="cover" href="title.html" media-type="application/xhtml+xml"/>
    <item id="content" href="%s.html" media-type="application/xhtml+xml"/>
    <item id="css" href="styles.css" media-type="text/css"/>
    %s
  </manifest>
  <spine toc="ncx">
    <itemref idref="cover" />
    <itemref idref="content"/>
    %s
  </spine>
  <guide>
    <reference href="title.html" type="cover" title="Cover"/>
  </guide>
</package>"""

toc_ncx = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>Movie Plot</text>
  </docTitle>
  <navMap>
    <navPoint id="navpoint-1" playOrder="1">
      <navLabel>
        <text>Book cover</text>
      </navLabel>
      <content src="title.html"/>
    </navPoint>
    <navPoint id="navpoint-2" playOrder="2">
      <navLabel>
        <text>%s</text>
      </navLabel>
      <content src="%s.html"/>
      %s
    </navPoint>
  </navMap>
</ncx>"""

title_html = """<!DOCTYPE html>
<html>
<head>
	<title>Title</title>
</head>
<body style = "text-align: center;">
	<h1>%s</h1>
	<p>Python Documentation</p>
</body>
</html>"""

styles_css = """
pre {
	background-color : #a4a4a4;
}
"""

def printEpub(htmlcode="", modname="", structureData={}, sectionPages=[]):
	epub = zipfile.ZipFile('epubs/%s.epub' % modname, 'w')
	epub.writestr("mimetype", "application/epub+zip")
	epub.writestr("OEBPS/%s.html" % modname, htmlcode)
	epub.writestr("OEBPS/content.opf", content_opf % (modname, modname, structureData['manifest'], structureData['spine']))
	epub.writestr("META-INF/container.xml", container_xml)
	epub.writestr("OEBPS/toc.ncx", toc_ncx % (modname, modname, structureData['toc']))
	epub.writestr("OEBPS/title.html", title_html % modname)
	epub.writestr("OEBPS/styles.css", styles_css)

	i = 1
	for page in sectionPages:
		epub.writestr("OEBPS/s%s.html" % i, page)
		i += 1