from spamlogic import tfidf,model,transform_text
from flask import Flask, render_template, request
import cx_Oracle

# con = cx_Oracle.connect("hr/hr@localhost:1521/xe")
con="postgres://qjexkzwvldznoc:db906085e24b59ec585b760df1a4850ac89394849c3808098a0f2b5e810b661a@ec2-34-234-240-121.compute-1.amazonaws.com:5432/d1skrr0ji02sfm"
cursor = con.cursor()
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
@app.route('/myForm', methods=['GET','POST'])
def myForm():
    if request.method == 'POST':
        uname = request.form.get("uname")
        email = request.form.get("email")
        cnumber = request.form.get("cnumber")
        password = request.form.get("password")
        # print(uname,email,cnumber,password)
        ins = '''insert into UserInfo(uname,email,cnumber,password)
                                                    values('{}','{}','{}','{}')
                                              '''.format(uname,email,cnumber,password)
        cursor.execute(ins)
        con.commit()
    return render_template('signup.html')

@app.route('/signin',  methods=['GET','POST'])
def signin():
    if request.method == 'POST':

        uname = request.form.get("uname")
        password = request.form.get("password")
        cursor.execute("select password from UserInfo where uname='{}'".format(uname))
        password_input = next(cursor)[0]

        if password == password_input:
            return render_template('spamworld.html')

        else:
            return render_template('errorsignin.html')
    return render_template('signin.html')

@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        emailtext = request.form.get("emailtext")
        transform_email = transform_text(emailtext)
        vector_input = tfidf.transform([transform_email])
        result1 = model.predict(vector_input)[0]

        if result1 == 1:
            return render_template('spamworld.html',result="SPAM",useremail=emailtext)

        else:
            return render_template('spamworld.html',result="NOT-SPAM",useremail=emailtext)


if __name__ == "__main__":
    app.run()






