import logging
import csv
import argparse
import sys



logging.basicConfig(filename="output.log",level=logging.DEBUG)


def put(name,snippet,filename):
	""" Store a snippet with an associated name in the CSV file """
	logging.info("Writing {!r}:{!r} to {!r}".format(name, snippet, filename))
	logging.debug("Opening file")
	with open(filename, "a") as f:
		writer = csv.writer(f)
		logging.debug("Writing snippet to file")
		writer.writerow([name,snippet])
	logging.debug("Write successful")
	return name, snippet

def get(name,filename):
	logging.info("Retrieving snippet for {} from {}".format(name, filename))
	logging.debug("Open file to read")
	with open(filename, "rb") as f:
		reader = csv.reader(f)
		for first, second in reader:
			if first == name:
				print "snippet for {} is {}".format(name, second)



def make_parser():
	"""command line parser """
	logging.info("Constructing parser")
	description = "Store and retrieve snippets of text"
	parser = argparse.ArgumentParser(description=description)
	
	subparsers = parser.add_subparsers(dest="command", help="Available commands")
	logging.debug("Constructing put subparser")
	put_parser = subparsers.add_parser("put", help="Store a snippet")
	put_parser.add_argument("name", help="The name of the snippet")
	put_parser.add_argument("snippet", help="The snippet text")
	put_parser.add_argument("filename", default="snippets.csv", nargs="?", help="The snippet filename")
	
	logging.debug("Constructing get subparser")
	get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
	get_parser.add_argument("name", help="The name of the snippet")
	get_parser.add_argument("filename", default="snippets.csv",nargs="?", help="The snippet filename")
	
	return parser

def main():
	logging.info("Starting snippets")
	parser = make_parser()
	arguments = parser.parse_args(sys.argv[1:])
	
	arguments = vars(arguments)
	command = arguments.pop("command")
	
	if command == "put":
		name, snippet = put(**arguments)
		print "Stored {!r} as {!r}".format(snippet, name)
	
	try:
		if command == "get":
			name, snippet = get(**arguments)
			print "retrieved {} from {}".format(snippet, name)
	except TypeError:
		print "end of file"
	except:
		print "crazy error:", sys.exc_info()[0]
		raise

if __name__ == "__main__":
	main()


