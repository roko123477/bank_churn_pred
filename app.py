from flask import Flask,render_template,request
from tensorflow import keras
from keras.models import load_model
import numpy as np

app=Flask(__name__)
model=load_model("churn1.h5")

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/sub",methods=['POST'])   
def predict():
    if(request.method=='POST'):
        cr_score=int(request.form['credscore'])
        gender=int(request.form['uigen'])
        age=int(request.form['age'])
        tenure=int(request.form['tenure'])
        balance=float(request.form['bal'])
        no_of_products=int(request.form['uinop'])
        has_cr_card=int(request.form['uicrcard'])
        active_mem=int(request.form['uiactive'])
        salary=float(request.form['salary'])
        location=request.form['loc']

        if(location=='france'):
            locate=[1,0]
        elif(location=='germany'):
            locate=[0,1]    
        else:
            locate=[0,0]

        cr_score=(cr_score-350)/500
        age=(age-18)/(84-18)
        tenure=tenure/10
        balance=balance/250898.09
        no_of_products=(no_of_products-1)/3
        salary=(salary-11.58)/(199808.1-11.58)
        
        output=model.predict(np.array([[cr_score,gender,age,tenure,balance,no_of_products,has_cr_card,active_mem,salary,locate[0],locate[1]]]))
        if(output[0][0]>0.5):
            val="Customer will leave bank"
        else:
            val="Customer will not leave bank"    
        return render_template("index.html",n=val)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)