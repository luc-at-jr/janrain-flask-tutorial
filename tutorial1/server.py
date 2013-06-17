from flask import Flask, render_template, request

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

janrain_engage_root_url = "https://rpxnow.com/api/v2/auth_info"

@app.route('/')
def index():
	return render_template('index.jade')

@app.route('/engage_callback_url', methods=['POST'])
def engage_callback():
	token = request.form['token']
	engage_api_params = {
		'apiKey': os.environ['JANRAIN_ENGAGE_API_KEY'],
		'token': token
	}
	user_data = requests.get(janrain_engage_root_url, params=engage_api_params)
	auth_info = user_data.json()
	profile = auth_info['profile']
	name = profile['name']['formatted']
	store_user_data_in_postgres(name)
	return render_template('logged_in.html', name=name)

app.run(debug=True, port=3000)