from toepub import toEpub

def console_tool():
	book = toEpub()
	print "\nePubPythonDocs\n==============\nRequesting page...\n"
	book.get_html()
	book.get_metadata()
	book.generate_struct()
	book.writeEpub()
	print "\nEpub generated successfully"

console_tool()