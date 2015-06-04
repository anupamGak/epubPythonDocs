from lxml import html
import requests
import re
from pager import pager
from printepub import printEpub

reHeadlink = re.compile('<a class="headerlink".+?<\/a>')

modname = raw_input("Enter a module : ")
pageresponse = requests.get("https://docs.python.org/2/library/%s.html" % modname)
modpage = html.fromstring(pageresponse.text)
modpage = modpage.xpath("//div[@class='body']")[0]

title = modpage.xpath("//h1/text()")
title[0] = modname
title = "".join(title)

sectionPages = []
manifest = ""
spine = ""
toc = ""
i = 1
sections = modpage.xpath("div/div[@class='section']")
for section in sections:
	soup = html.tostring(section)
	soup = re.sub(reHeadlink, "", soup)
	sectionTitle = re.findall("(?<= )[A-Za-z ]+", section.xpath("h2/text()")[0])[0]
	sectionPages.append(pager(soup, i))
	manifest += '<item id="html-%s" href="s%s.html" media-type="application/xhtml+xml"/>' % (i, i)
	spine += '<itemref idref="html-%s"/>' % i
	toc += """<navPoint id="navpoint-%s" playOrder="%s">
      <navLabel>
        <text>%s</text>
      </navLabel>
      <content src="s%s.html"/>
    </navPoint>""" % (i+2, i+2, sectionTitle, i)
	i += 1

structureData = {
	"manifest" : manifest,
	"spine" : spine,
	"toc" : toc
}

metadata = {
	"title" : title,
	"modname" : modname
}

soup = html.tostring(modpage)
soup = re.sub(reHeadlink, "", soup)

ePage = pager(soup, modname)
printEpub(ePage, modname, structureData, sectionPages)