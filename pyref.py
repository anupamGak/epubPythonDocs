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

metadata = {
	"title" : title.encode('ascii','ignore'),
	"modname" : modname
}

sections = modpage.xpath("div/div[@class='section']")
toc = ""
for section in sections:
	sectmeta = {
		"id" : section.xpath("@id")[0],
		"title" : section.xpath("h2/text()")[0],
		"modname" : modname
	}
	sectmeta['title'] = " ".join(re.findall("[a-zA-Z]+", sectmeta['title']))
	toc += """<navPoint>
	  <navLabel>
        <text>%(title)s</text>
      </navLabel>
      <content src="%(modname)s.html#%(id)s"/>
    </navPoint>""" % sectmeta



metadata['toc'] = toc

soup = html.tostring(modpage)
soup = re.sub(reHeadlink, "", soup)

ePage = pager(soup, modname)
printEpub(ePage, metadata)
print "Done!"