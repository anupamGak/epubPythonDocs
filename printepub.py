import zipfile
from lxml import etree
import re

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
	<dc:title>%(modname)s</dc:title>
	<dc:creator>Python  Documentation</dc:creator>
	<dc:identifier id="bookid">urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658</dc:identifier>
	<dc:language>en-US</dc:language>
	<meta name="cover" content="cover-image" />
  </metadata>
  <manifest>
	<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
	<item id="cover" href="title.html" media-type="application/xhtml+xml"/>
	<item id="content" href="%(modname)s.html" media-type="application/xhtml+xml"/>
	%(manifest)s
	<!--manifest-->
	<item id="cover-image" href="images/cover.png" media-type="image/png"/>
	<item id="css" href="styles.css" media-type="text/css"
  </manifest>
  <spine toc="ncx">
	<itemref idref="cover" />
	<itemref idref="content"/>
	%(spine)s
	<!--spine-->
  </spine>
  <guide>
	<reference href="title.html" type="title-page" title="Title"/>
  </guide>
</package>"""

toc_ncx = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
				 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
	<meta name="dtb:uid" content="urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658"/>
	<meta name="dtb:depth" content="2"/>
	<meta name="dtb:totalPageCount" content="0"/>
	<meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
	<text>Python Docs</text>
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
		<text>%(modname)s</text>
	  </navLabel>
	  <content src="%(modname)s.html"/>
		%(toc)s
		<!--toc-->
	</navPoint>
  </navMap>
</ncx>"""

title_html = """<!DOCTYPE html>
<html>
<head>
	<title>Title</title>
</head>
<body style = "text-align: center;">
	<h1>%(modname)s</h1>
	<p>Python Documentation</p>
</body>
</html>"""

styles_css = """
pre {
	font-family : monospace;
	background-color : #a4a4a4;
	overflow : auto;
	font-size : 0.8em;
}
h1 {
	font-size : 2.5em;
}
.descname {
	font-weight : bold;
	font-size : 1.4em;
}"""


def filler(sectdata=[], navpoint=0):
	manifest = ""
	spine = ""
	toc = ""
	for data in sectdata:
		data['navpoint'] = data['no'] + 2 + navpoint
		manifest += '<item id="html-%(modname)s%(no)s" href="%(modname)s%(no)s.html" media-type="application/xhtml+xml"/>' % data
		spine += '<itemref idref="html-%(modname)s%(no)s"/>' % data
		toc += """<navPoint id="navpoint-%(navpoint)s" playOrder="%(navpoint)s">
					<navLabel>
						<text>%(title)s</text>
					</navLabel>
					<content src="%(modname)s%(no)s.html"/>
				  </navPoint>""" % data

	filling = {
		"manifest" : manifest,
		"spine" : spine,
		"toc" : toc
	}
	return filling


def printEpub(htmlcode="", metadata={}, sectdata=[]):

	metadata.update(filler(sectdata))
	epub = zipfile.ZipFile('epubs/%s.epub' % metadata['modname'], 'w')
	epub.writestr("mimetype", "application/epub+zip")
	epub.writestr("OEBPS/%s.html" % metadata['modname'], htmlcode)
	epub.writestr("OEBPS/content.opf", content_opf % metadata)
	epub.writestr("META-INF/container.xml", container_xml)
	epub.writestr("OEBPS/toc.ncx", toc_ncx % metadata)
	epub.writestr("OEBPS/title.html", title_html % metadata)
	epub.writestr("OEBPS/styles.css", styles_css)
	epub.write("cover.png", "OEBPS/images/cover.png")

	for data in sectdata:
		epub.writestr("OEBPS/%s%d.html" % (metadata['modname'], data['no']), data['page'])

def addtoEpub(htmlcode="", metadata={}, sectdata=[]):
	epub = zipfile.ZipFile('epubs/%s.epub' % metadata['modname'], 'a')
	nons = re.sub('xmlns=".+?"', "", epub.read("OEBPS/toc.ncx"))
	toc = etree.fromstring(nons)
	navpoints = len(toc.xpath("//navPoint"))

	toc_file = epub.read('OEBPS/toc.ncx')
	toc_file = toc_file.replace("<!--toc-->", "%(toc)s")

	metadata.update(filler(sectdata))