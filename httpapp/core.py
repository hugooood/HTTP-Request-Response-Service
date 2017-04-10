# -*- coding: utf-8 -*-

from flask import Flask,render_template,jsonify as flask_jsonify,request
from werkzeug.datastructures import MultiDict

#自定义模组
from helpers import get_headers,get_dict,status_code

def jsonify(*args,**kwargs):
	response = flask_jsonify(*args,**kwargs)
	#-----------------
	#1.判断作用是什么？
	#2.b有什么作用？
	#-----------------
	if not response.data.endswith(b'\n'):
	 	response.data += b'\n'
	return response

app = Flask(__name__)

# ------
# Routes
# ------
@app.route('/')
def view_landing_page():
	return render_template('index.html')

@app.route('/ip')
def view_origin():
	"""Returns Origin IP."""				

	return jsonify(origin=request.headers.get('X-Forwarded-For',#请求头
				request.remote_addr))

@app.route('/user-agent')
def view_user_agent():
	"""Returns User-Agent"""
	headers = get_headers()
	return jsonify({'user-agent':headers['user-agent']})

@app.route('/headers')
def view_headers():
	"""Returns HTTP HEADERS."""
	return jsonify(get_dict('headers'))

@app.route('/get',methods=('GET',))
def view_get():
	"""Returns GET Data."""
	return jsonify(get_dict('url','args','headers','origin'))

@app.route('/post',methods=('POST',))
def view_post():
	"""Return POST Data."""
	return jsonify(get_dict('url','args','form','data','origin','headers','files','json'))

@app.route('/patch',methods=('PATCH',))
def view_patch():
	"""Return PATCH Data."""
	return jsonify(get_dict('url','args','form','data','origin','headers','files','json'))

@app.route('/encoding/utf-8')
def encoding():
	return render_template('utf-8-demo.txt')

@app.route('/gzip')
def view_gzip_encoded_content():
	"""Returns Gzip-Encoded Data."""
	return jsonify(get_dict('origin','headers',method=request.method,gzipped=True))

@app.route('/deflate')
def view_deflate_encode_content():
	"""Returns Defalte-Encoded Data."""
	return jsonify(get_dict('origin','headers',method=request.method,deflated=True))

@app.route('/brotli')
def view_brotli_encode_content():
	"""Returns Brotli-Encoded Data."""
	return jsonify(get_dict('origin','headers',method=request.method,brotli=True))

@app.route('/status/<codes>',methods=['GET','POST','PUT','DELETE','PATCH','TRACE'])
def view_status_code(codes):
	"""Return status code or random status code if more than one are given"""
	if ',' not in codes:
		try:
			code = int(codes)
		except ValueError:
			return Response('Invalid status code',status=400)
		return status_code(code)

	choices = []
	for choice in codes.split(','):
		if ':' not in choice:
			code = choice
			weight = 1
		else:
			code, weight = choice.split(':')
		try:
			choices.append((int(code),float(weight)))
		except ValueError:
			return Response('Invalid status code',status=400)

	code = weighted_choice(choices)

	return status_code(code)		

@app.route('/response-headers')
def response_headers():
	"""Returns a set of response headers from the query string """
	headers = MultiDict(request.args.items(multi=True))
	response = jsonify(list(headers.lists()))

	while True:
		original_data = response.data
		d = {}
		for key in response.headers.keys():
			value = response.headers.get_all(key)
			if len(value) == 1:
				value = value[0]
			d[key] = value
		response = jsonify(d)
		for key,value in headers.items(multi=True):
			response.headers.add(key,value)
		response_has_changed = response.data != original_data
		if not response_has_changed:
			break
	return response


if __name__ == '__main__':
	app.run(debug=True)