def pager(soup="", title=""):
	code = """<!DOCTYPE html>
				<html>
				<head>
					<title>%s - Documentation</title>
				</head>
				<body>
				%s
				</body>
				</html>""" % (title, soup)

	with open('modhtmls/%s.htm' % title, 'w') as f:
		f.write(code)
	return code