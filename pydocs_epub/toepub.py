import zipfile
from lxml import html
import requests
import os
import re
import argparse

class toEpub:
	metadata = {}
	container_xml = ""
	content_opf = ""
	toc_ncx = ""
	title_html = ""
	styles_css = ""
	new_epub = True
	pagehead = ""
	pagefrag = ""
	pagehtml = ""

	def __init__(self):
		with open('resources/container.xml', 'r') as f:
			self.container_xml = f.read()
		with open('resources/content.opf', 'r') as f:
			self.content_opf = f.read()
		with open('resources/toc.ncx', 'r') as f:
			self.toc_ncx = f.read()
		with open('resources/title.html', 'r') as f:
			self.title_html = f.read()
		with open('resources/styles.css', 'r') as f:
			self.styles_css = f.read()
		with open('resources/pagehead.html', 'r') as f:
			self.pagehead = f.read()
		new_epub = True

	def get_args(self):
		parser = argparse.ArgumentParser(
			description="Stores the Python Documentation of the module in an epub file")

		parser.add_argument("module", type=str)
		parser.add_argument("-a", "--app", action="store_true", help="Append to an existing epub file")
		args = parser.parse_args()

		self.metadata['name'] = args.module
		if args.app:
			self.new_epub = False

	def get_html(self):
		resp = requests.get("https://docs.python.org/2/library/%s.html" % self.metadata['name'])
		tree = html.fromstring(resp.text)
		tree = tree.xpath("//div[@class='body']/div[1]")[0]
		self.pagefrag = html.tostring(tree)

		reHeadlink = re.compile('<a class="headerlink".+?<\/a>')
		self.pagefrag = re.sub(reHeadlink, "", self.pagefrag)

		self.pagehtml = self.pagehead % (self.metadata['name'], self.pagefrag)

	def get_metadata(self):
		tree = html.fromstring(self.pagefrag)

		reCountflag = re.compile(r"<!--(\d{1,2})-->")
		self.metadata.update({
				"sectIDs" : tree.xpath("div[@class='section']/@id"),
				"sectTtl" : tree.xpath("div[@class='section']/h2/text()"),
				"count" : str(int(re.findall(reCountflag, self.content_opf)[0]) + 1).zfill(2),
				"navcount" : int(re.findall(reCountflag, self.toc_ncx)[0]) + 1
			})

	def generate_struct(self):
		metadata = self.metadata

		reCountflag = re.compile(r"<!--(\d{1,2})-->")
		self.content_opf = re.sub(reCountflag, "", self.content_opf)
		self.toc_ncx = re.sub(reCountflag, "", self.toc_ncx)

		reFlag = re.compile(r"<!--([a-z]+)-->")
		self.content_opf = re.sub(reFlag, r"%(\1)s", self.content_opf)
		self.toc_ncx = re.sub(reFlag, r"%(\1)s", self.toc_ncx)

		manifest = """<item id="module-%(count)s" href="module-%(count)s.html" media-type="application/xhtml+xml"/>
		<!--manifest-->
		<!--%(count)s-->""" % metadata

		spine = """<itemref idref="module-%(count)s"/>
		<!--spine-->""" % metadata

		toc = """<navPoint id="navpoint-%(navcount)s" playOrder="%(navcount)s">
			  <navLabel>
				<text>%(name)s</text>
			  </navLabel>
			  <content src="module-%(count)s.html"/>
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

		struct = {
			"manifest" : manifest,
			"spine" : spine,
			"toc" : toc
		}

		self.content_opf = self.content_opf % struct
		self.toc_ncx = self.toc_ncx % struct

	def writeEpub(self):
		epub = zipfile.ZipFile('epubs/newmeta.epub', 'w')
		epub.writestr("mimetype", "application/epub+zip")
		epub.writestr("OEBPS/module-01.html", self.pagehtml)
		epub.writestr("OEBPS/content.opf", self.content_opf)
		epub.writestr("META-INF/container.xml", self.container_xml)
		epub.writestr("OEBPS/toc.ncx", self.toc_ncx)
		epub.writestr("OEBPS/title.html", self.title_html)
		epub.writestr("OEBPS/styles.css", self.styles_css)

	def printer(self):
		with open('con.opf', 'w') as f:
			f.write(self.content_opf)
		with open('toctoc.ncx', 'w') as f:
			f.write(self.toc_ncx)

book = toEpub()

book.metadata['name'] = "os"

book.get_html()
book.get_metadata()
book.generate_struct()
book.writeEpub()