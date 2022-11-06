from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

questions = [["does your head hurt?","headache","guess"]]
def dataDump(todump):
    with open('test.json','w') as f:
        tojson={'json':todump}
        json.dump(tojson, f)
def dataLoad():
    with open('test.json') as f:
        fromjson=json.load(f)
        return fromjson['json']

@app.route('/')
@app.route('/index', methods=['POST','GET'])
def index():
    position = 0
    if request.method=='POST':
        x=request.form
        print(x)
        if 'Symptom Analysis' in request.form.values():
            return redirect(f"/{position}")
        elif "I'm a healthcare professional" in request.form.values():
            return redirect('/professional')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')
@app.route('/<int:position>',methods=['POST','GET'])
def doStuff(position):
    questions=dataLoad()
    if request.method=='POST':
        if request.form['yn'] == 'yes':
            if isinstance(questions[position][1],int) and questions[position][1] != -1:
                position = questions[position][1]
                return redirect(f"/{position}")
            elif questions[position][1] == -1:
                return redirect(f'/createy/{position}')
            else:
                return redirect(f"addnew/{position}/{questions[position][1]}")
        else:
            if isinstance(questions[position][2],int) and questions[position][2] != -1:
                position = questions[position][2]
                return redirect(f"/{position}")
            elif questions[position][2] == -1:
                return redirect(f"create/{position}")
            else:
                return redirect(f'addnew/{position}/{questions[position][2]}')
    else:
        print(position)
        return render_template('yesno.html',question=questions[position][0], position=position)

@app.route('/addnew/<int:position>/<illness>',methods=['POST','GET'])
def addnew(position,illness):
    if request.method=='POST':
        if request.form['check'] != 'yes':
            return redirect(f'/createy/{position}')
        else:
            return redirect(f'/found/{illness}')
    else:
        return render_template('addnew.html',illness=illness,position=f'{position}/{illness}')

@app.route("/createy/<int:position>",methods=['POST','GET'])
def createy(position):
    questions=dataLoad()
    if request.method=='POST':
        animal=request.form['illness']
        question=request.form['question']
        questions.append([question,animal,questions[position][1]])
        questions[position][1] = len(questions)-1
        dataDump(questions)
        return redirect('/index')
    else:
        return render_template('add.html',goto=f'createy/{position}')

@app.route('/create/<int:position>',methods=['POST','GET'])
def create(position):
    if request.method=='POST':
        animal=request.form['illness']
        question=request.form['question']
        questions.append([question,animal,questions[position][2]])
        questions[position][2] = len(questions)-1
        dataDump(questions)
        return redirect('/index')
    else:
        return render_template('add.html',goto=f'create/{position}')

@app.route('/found/<illness>', methods=["POST","GET"])
def found(illness):
    if request.method == "POST":
        return redirect("/index")
    else:
        with open('therapists.json') as f:
            therapists = json.load(f)
        useful={}
        for i in therapists:
            print(i)
            if therapists[i]["illness"] == illness:
                useful[i]=therapists[i]
        return render_template('found.html',illness=illness,therapists=useful)

@app.route('/professional',methods=["POST","GET"])
def professional():
    if request.method=="POST":
        with open('therapists.json') as f:
            therapists = json.load(f)
        therapists[request.form['name']]={'illness':request.form['illness'],'location':request.form['location'],'contact':request.form['contact']}
        with open('therapists.json',"w") as f:
            json.dump(therapists,f)
            return redirect('/index')
    else:
        questions = dataLoad()
        illnesses=[]
        for i in questions:
            for j in i[1:]:
                if isinstance(j,int) == False:
                    illnesses.append(j)
        return render_template('therapist.html',illnesses=illnesses)

app.run(host='0.0.0.0', port=8001)