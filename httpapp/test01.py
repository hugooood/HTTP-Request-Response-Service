from flask import Flask,render_template,jsonify as flask_jsonify,request
from structures import CaseInsensitiveDict

ENV_HEADERS = (
    'X-Varnish',
    'X-Request-Start',
    'X-Heroku-Queue-Depth',
    'X-Real-Ip',
    'X-Forwarded-Proto',
    'X-Forwarded-Protocol',
    'X-Forwarded-Ssl',
    'X-Heroku-Queue-Wait-Time',
    'X-Forwarded-For',
    'X-Heroku-Dynos-In-Use',
    'X-Forwarded-For',
    'X-Forwarded-Protocol',
    'X-Forwarded-Port',
    'X-Request-Id',
    'Via',
    'Total-Route-Time',
    'Connect-Time'
)

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


def get_headers(hide_env=True):
    """Returns headers dict from request context."""

    #print(request.headers.items())
    headers = dict(request.headers.items())
    #print('headers:',headers)
    if hide_env and ('show_env' not in request.args):
        print('node1')
        for key in ENV_HEADERS:
            print('node2')
            try:
                print('node3')
                del headers[key]
            except KeyError:
                print('node4')
                pass
    print('headers:',headers)
    return CaseInsensitiveDict(headers.items())

@app.route('/user-agent')
def view_user_agent():
    headers = get_headers()
    print('get_headers:',get_headers())
    return jsonify({'user-agent':headers['user-agent']})

if __name__ == '__main__':
    app.run(debug=True)