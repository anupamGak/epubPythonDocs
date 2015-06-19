import zipfile
import re
import os

reAbbr = re.compile("(?<= )[A-Z]")
reFlag = re.compile(r"<!--([a-z]+)-->")
reCountflag = re.compile(r"<!--(\d{1,2})-->")

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
	<dc:title>Python Reference</dc:title>
	<dc:creator>Python Documentation</dc:creator>
	<dc:identifier id="bookid">urn:uuid:0cc33cbd-94e2-49c1-909a-72ae16bc2658</dc:identifier>
	<dc:language>en-US</dc:language>
  </metadata>
  <manifest>
	<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
	<item id="cover" href="title.html" media-type="application/xhtml+xml"/>
	<item id="css" href="styles.css" media-type="text/css" />
	<!--manifest-->
	<!--00-->
  </manifest>
  <spine toc="ncx">
	<itemref idref="cover"/>
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
	<!--toc-->
	<!--1-->
  </navMap>
</ncx>"""

title_html = """<!DOCTYPE html>
<html>
<head>
	<title>Python Reference</title>
</head>
<body style = "text-align: center;">
	<h1>Python Reference</h1>
	<p>Python Documentation</p>
</body>
</html>"""

styles_css = """
pre {
	background-color: #a4a4a4;
	font-family: monospace;
	overflow: auto;
	font-size: 0.85em;
}

.descname {
	font-weight: bold;
	font-size: 1.4em;
}

.section {
	page-break-before: always;
}
"""

def filler(metadata={}):
	manifest = """<item id="module-%(count)s" href="module-%(count)s.html" media-type="application/xhtml+xml"/>
	<!--manifest-->
	<!--%(count)s-->""" % metadata

	spine = """<itemref idref="module-%(count)s"/>
	<!--spine-->""" % metadata

	toc = """<navPoint id="navpoint-%(navcount)s" playOrder="%(navcount)s">
		  <navLabel>
			<text>%(modname)s</text>
		  </navLabel>
		  <content src="module-%(count)s.html#"/>
		  	""" % metadata
	for i in range(len(metadata['sectIDs'])):
		metadata['navcount'] += 1
		metadata['sectID'] = metadata['sectIDs'][i]
		metadata['ttl'] = re.findall(r"\d\.\s(.+)", metadata['sectTtl'][i])[0]
		toc += """<navPoint id="navpoint-%(navcount)s" playOrder="%(navcount)s">
		  <navLabel>
			<text>%(ttl)s</text>
		  </navLabel>
		  <content src="module-%(count)s.html#%(sectID)s"/>
		</navPoint>""" % metadata

	toc += """</navpoint>
	<!--toc-->
	<!--%(navcount)s-->""" % metadata

	return {
		"manifest" : manifest,
		"spine" : spine,
		"toc" : toc
	}

def printEpub(htmlcode="", metadata={}, append=True):
	global content_opf, toc_ncx
	if append:
		epubin = zipfile.ZipFile('epubs/PyReference.epub', 'r')

		content_opf = epubin.read("OEBPS/content.opf")
		toc_ncx = epubin.read("OEBPS/toc.ncx")

		metadata['count'] = str(int(re.findall(reCountflag, content_opf)[0]) + 1).zfill(2)
		metadata['navcount'] = int(re.findall(reCountflag, toc_ncx)[0]) + 1
		metadata.update(filler(metadata))

		content_opf = re.sub(reCountflag, "", content_opf)
		toc_ncx = re.sub(reCountflag, "", toc_ncx)

		content_opf = re.sub(reFlag, r"%(\1)s", content_opf)
		toc_ncx = re.sub(reFlag, r"%(\1)s", toc_ncx)

		content_opf = content_opf % metadata
		toc_ncx = toc_ncx % metadata


		epubout = zipfile.ZipFile('epubs/newfile.epub', 'w')
		epubout.writestr("OEBPS/content.opf", content_opf)
		epubout.writestr("OEBPS/toc.ncx", toc_ncx)
		epubout.writestr("mimetype", "application/epub+zip")
		epubout.writestr("META-INF/container.xml", container_xml)
		epubout.writestr("OEBPS/styles.css", styles_css)
		epubout.writestr("OEBPS/module-%(count)s.html" % metadata, htmlcode)

		filenames = [i for i in epubin.namelist() if ".html" in i]
		for filename in filenames:
			epubout.writestr(filename, epubin.read(filename))

		epubin.close()
		epubout.close()

		os.rename("epubs/newfile.epub", "epubs/PyReference.epub")

	else:
		metadata['count'] = str(int(re.findall(reCountflag, content_opf)[0]) + 1).zfill(2)
		metadata['navcount'] = int(re.findall(reCountflag, toc_ncx)[0]) + 1
		metadata.update(filler(metadata))

		content_opf = re.sub(reCountflag, "", content_opf)
		toc_ncx = re.sub(reCountflag, "", toc_ncx)

		content_opf = re.sub(reFlag, r"%(\1)s", content_opf)
		toc_ncx = re.sub(reFlag, r"%(\1)s", toc_ncx)

		epub = zipfile.ZipFile('epubs/PyReference.epub', 'w')
		epub.writestr("mimetype", "application/epub+zip")
		epub.writestr("OEBPS/module-01.html", htmlcode)
		epub.writestr("OEBPS/content.opf", content_opf % metadata)
		epub.writestr("META-INF/container.xml", container_xml)
		epub.writestr("OEBPS/toc.ncx", toc_ncx % metadata)
		epub.writestr("OEBPS/title.html", title_html % metadata)
		epub.writestr("OEBPS/styles.css", styles_css)