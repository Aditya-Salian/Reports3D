from flask import Flask, render_template, request, redirect, url_for
from DB_functions import *
from FinalCodeFunctions import Create3DModel, TextureEdit, removefiles
# from werkzeug import secure_filename
# from FinalCodeFunctions import Create3DModel, TextureEdit
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/share/<p_id>', methods=['GET', 'POST'])
def output_from_url(p_id):
   	 return render_template('output.html', f1 = f'{p_id}modelnew.gltf', f2 = f'{p_id}modelnew.usdz')


@app.route('/output', methods=['GET', 'POST'])
def output():
	if request.method == 'POST':
		p_id = request.form['p_id']
		return render_template('output.html', f1 = f'{p_id}modelnew.gltf', f2 = f'{p_id}modelnew.usdz')

@app.route('/login', methods=['GET', 'POST'])
def logindef():
	if request.method == 'POST':
		email=request.form["email"]
		password=request.form["password"]
		username=request.form["username"]
		values_to_insert=(username, email, password)
		doctor_insert(con,values_to_insert)
	return render_template('login.html')


d_id=0
@app.route('/loginuser', methods=['GET', 'POST'])
def loginuserdef():
	if request.method == 'POST':
		email=request.form["email_id"] 
		password=request.form["password"] #pwd is test123
		global d_id
		access, d_id=login(con, email, password)
		if access:
			try:
				rows=find_patient(con, d_id)
				return render_template('dashboard.html', rows=rows)
			except:
				pass
				# return render_template('login.html')     CHECK THIS
		else:
			return redirect('/login')


'''Registering new patient into database'''
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		p_id=request.form['p_id']
		name=request.form['name']
		comment=request.form['comment']
		file1 = request.files['file1']
		file1.save((file1.filename))
		file2 = request.files['file2']
		file2.save((file2.filename))
		flair = file1.filename
		t2 = file1.filename
		Create3DModel(flair, t2, p_id)
		path_to_gltf , path_to_usdz = TextureEdit(p_id)
		'''insert into database'''
		values_to_insert=(p_id, d_id, name, comment, path_to_gltf)
		patient_insert(con, values_to_insert)
		removefiles(flair,t2)
		

		# gltf_file_name = path_to_gltf[path_to_gltf.rfind('/')+1::]

		# usdz_file_name = path_to_usdz[path_to_usdz.rfind('/')+1::]
		


		# file1 = request.files['file1']
		# file1.save(secure_filename(file1.filename))
		# file2 = request.files['file2']
		# file2.save(secure_filename(file2.filename))
		'''have hardcoded the local link right now, d_id retrieved from login'''		
		# values_to_insert=(p_id, d_id, name, comment,path)
		'''insert into database'''
		# patient_insert(con, values_to_insert)
		# Create3DModel()
		# TextureEdit()
	# return f"<h1>TEMPORARY BECUASE IDK HOW TO REDIRECT TO 3D MODEL</h1>"
	#return render_template('output.html', f1 = path_to_gltf, f2 = path_to_usdz)
	# return render_template('output.html', f1 = gltf_file_name, f2 = usdz_file_name)
	return render_template('output.html', f1 = path_to_gltf, f2 = path_to_usdz)

		
if __name__ == '__main__':
	'''Mandatory functions to run'''
	con = create_sql_connection()
	check(con)
	create_sql_table(con)
	app.run(port=5000,debug = True)



