def parse_query_string(query_string):
	arr = query_string.split('&')
	result = ""
	for i in arr:
		result += i + '\n'
	return result

def app(environ, start_response):
	"""Simplest possible application object"""
	#data = b'Hello, World!\n'
	status = '200 OK'
	data = str.encode(parse_query_string(environ['QUERY_STRING']))
	response_headers = [
		('Content-type','text/plain'),
		('Content-Length', str(len(data)))
	]
	start_response(status, response_headers)
	return iter([data])
