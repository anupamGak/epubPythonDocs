from lxml import html
import requests
import re
import argparse
from pager import pager
from printepub import printEpub

parser = argparse.ArgumentParser(description="Stores the Python Documentation of the module in an epub file")

parser.add_argument("module", type=str)
parser.add_argument("-a", "--app", action="store_true", help="Append to an existing epub file")
args = parser.parse_args()

reHeadlink = re.compile('<a class="headerlink".+?<\/a>')

modname = args.module
pageresponse = requests.get("https://docs.python.org/2/library/%s.html" % modname)
modpage = html.fromstring(pageresponse.text)
modpage = modpage.xpath("//div[@class='body']/div[1]")[0]

title = modpage.xpath("//h1/text()")
title[0] = modname
title = "".join(title)

metadata = {
	"title" : title.encode('ascii','ignore'),
	"modname" : modname,
	"sectIDs" : modpage.xpath("div[@class='section']/@id"),
	"sectTtl" : modpage.xpath("div[@class='section']/h2/text()")
}

soup = html.tostring(modpage)
soup = re.sub(reHeadlink, "", soup)

ePage = pager(soup, modname)

if args.app:
	append = True
else:
	append = False
printEpub(ePage, metadata, append)
print "Done!"