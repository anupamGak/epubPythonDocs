def pager(soup="", title=""):
	code = """<!DOCTYPE html>
				<html>
				<head>
					<title>%s</title>
					<link rel="stylesheet" href="styles.css">
				</head>
				<body>
				%s
				</body>
				</html>""" % (title, soup)
	return code