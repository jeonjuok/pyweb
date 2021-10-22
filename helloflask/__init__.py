from flask import Flask, g, request, Response, make_response
from flask import session
from flask import render_template
from datetime import date, datetime, timedelta
from flask.helpers import make_response
from flask import Markup

app = Flask(__name__)
app.debug = True

# trim_blocks app config
app.jinja_env.trim_blocks = True

# Session start
app.config.update(
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days  cf. minutes=30
)
# Session end


@app.route('/')
def idx():
    return render_template('app.html', ttt='TestTTT')


# @app.route('/top100')
# def top100():
#     return render_template('application.html', title="MIN!!")




@app.route('/tmpl')
def tmpl():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print("h=", h)

    return render_template('index.html', title="Title", mu=h)


# Cookie + session start
@app.route('/wc') #요청 http://localhost:5000/wc?key=token&val=abc
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response('SET COOKIE')
    res.set_cookie(key, val)
    session['Token'] = '123X'
    return make_response(res)

@app.route('/rc') #요청 http://localhost:5000/rc?key=token
def rc():
    key = request.args.get('key') #token
    val = request.cookies.get(key) 
    return "cookie['" + key + "'] = " + val + ", " + session.get('Token')
    
# Cookie + session end


@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"


@app.route('/reqenv')
def reqenv():
    return ('asdfasdfasdfasdfasdfasdfasdf') % request.environ



# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans


@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)


# app.config['SERVER_NAME'] = 'local.com:5000'

# @app.route("/sd")
# def helloworld_local():
#     return "Hello Local.com!"

# @app.route("/sd", subdomain="g")
# def helloworld():
#     return "Hello G.Local.com!!!"




@app.route('/rp')
def rp():
    # q = request.args.get('q')
    q = request.args.getlist('q')
    return "q= %s" % str(q)


@app.route('/res1')
def res1():
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)



# WSGI(WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'), 
					('Content-Length', str(len(body))) ]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)


# @app.before_request
# def before_request():
#     print("before_request!!!")
#     g.str="한글"


@app.route("/gg")
def helloworld2():
    return "Hello Flask World!" + getattr(g, 'str', '111')



@app.route("/hello")
def helloworld():
    return "Hello Flask World!"
