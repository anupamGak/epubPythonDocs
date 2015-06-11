from lxml import html
import requests
import re
from pager import pager
import printepub

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

sectdata = []
for section in sections:
	soup = html.tostring(section)
	soup = re.sub(reHeadlink, "", soup)

	sectdict = {
		"modname" : modname,
		"title" : re.findall("(?<=\d. ).+", section.xpath("h2/text()")[0])[0],
		"no" : i,
		"page" : pager(soup, i)
	}
	sectdata.append(sectdict)
	i += 1

metadata = {
	"title" : title.encode('ascii','ignore'),
	"modname" : modname
}

intronodes = modpage.xpath("//h1/following-sibling::*")
soup = html.tostring(modpage.xpath("//h1")[0])
for node in intronodes:
	if not node.get('class') == "section":
		soup += html.tostring(node)
	else:
		break

soup = re.sub(reHeadlink, "", soup)
ePage = pager(soup, modname)

choice = raw_input("Create a new epub?[y/n]('n' under construction) :")
if choice == "y":
	printepub.printEpub(ePage, metadata, sectdata)
else:
	printepub.addtoEpub(ePage, metadata)
print "Done!"