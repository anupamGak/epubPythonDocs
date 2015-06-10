def pager(soup="", title=""):
	code = """<!DOCTYPE html>
				<html>
				<head>
					<title>%s - Documentation</title>
					<link rel="stylesheet" type="text/css" href="styles.css" />
				</head>
				<body>
				%s
				</body>
				</html>""" % (title, soup)

	with open('modhtmls/%s.htm' % title, 'w') as f:
		f.write(code)
	return code