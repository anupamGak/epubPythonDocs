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
	return code