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

	with open('modhtmls/s%s.htm' % title, 'w') as f:
		f.write(code)
	return code