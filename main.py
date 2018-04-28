from flask import request, redirect, render_template, flash, session
from app import app , db
from model import question_bank, User, test_result
from sqlalchemy.sql.expression import func, select


@app.route('/')
def index():
    return render_template('add_question.html')


@app.route('/add_question', methods = ['POST', 'GET'])
def addQuestion():
    if request.method == 'POST':
            grade = str.strip(request.form["grade"])
            subject = str.strip(request.form["subject"])
            question = str.strip(request.form["question"])
            detailed_answer = str.strip(request.form["detailed_answer"])
            choice_1 = str.strip(request.form["choice_1"])
            choice_2 = str.strip(request.form["choice_2"])
            choice_3 = str.strip(request.form["choice_3"])
            choice_4 = str.strip(request.form["choice_4"])
            correct_answer = str.strip(request.form["correct_answer"])
            new_question = question_bank(grade, subject, question, detailed_answer, choice_1, choice_2, choice_3, choice_4, correct_answer)
            db.session.add(new_question)
            db.session.commit()
            return render_template('add_question.html')
    else:
        return render_template('add_question.html')

@app.route('/update', methods = ['POST'])
def update():
            id = str.strip(request.form["id"])
            print("########################### " + id )
            edit_question = question_bank.query.filter_by(id=id).first()
            edit_question.grade = str.strip(request.form["grade"])
            edit_question.subject = str.strip(request.form["subject"])
            edit_question.question = str.strip(request.form["question"])
            edit_question.detailed_answer = str.strip(request.form["detailed_answer"])
            edit_question.choice_1 = str.strip(request.form["choice_1"])
            edit_question.choice_2 = str.strip(request.form["choice_2"])
            edit_question.choice_3 = str.strip(request.form["choice_3"])
            edit_question.choice_4 = str.strip(request.form["choice_4"])
            edit_question.correct_answer = str.strip(request.form["correct_answer"])
            #db.session.update(edit_question)
            db.session.commit()
            return redirect('/list_all')
    

@app.route('/list_all', methods=['GET'])
def list_all():
    questions_bank = question_bank.query.all()
    return render_template('list_question.html', questions_bank=questions_bank)

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    id = request.form["id"]
    edit_question = question_bank.query.filter_by(id=id).first()
    return render_template('edit.html', edit_question=edit_question)

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    
    if request.method == 'POST':
        
        
        if session.get('grade') and session.get('subject') :
            grade = session['grade']
            subject = session['subject']
        else:
            grade = str.strip(request.form["grade"])
            subject = str.strip(request.form["subject"])
            session['grade'] = grade
            session['subject'] = subject

        questionIdList =[]

        if session.get('questionIdList'):
            questionIdList = session['questionIdList']
            print(session['questionIdList'])
            questionId = questionIdList.pop()
            session['questionIdList'] = questionIdList
            
            questionForTest = question_bank.query.get(questionId)
            
            session['correctAnswer'] = questionForTest.correct_answer

        else:
            questions_bank = question_bank.query.filter_by(grade=grade).filter_by(subject=subject).all()
            
            questionForTest = questions_bank[0]
            
            session['correctAnswer'] = questionForTest.correct_answer

            for question in questions_bank :
                print (question.id)
                questionIdList.append(question.id)   
            
            session['questionIdList'] = questionIdList

        print(session['questionIdList'])
  
        return render_template('test.html', question=questionForTest )
        
    else:
        return render_template('login.html')



@app.route('/result', methods = ['POST'])
def result():
    #check the answer
    
    score = 0
    count = 0
    if session.get('count'):
        count = int(session['count'])
    else:
        session['count'] = 0

    count = count + 1
    session['count'] = count

    if  session.get('score') :
        score  = int(session['score'])
    else:
        session['score'] = 0    

    selectedAnswer = request.form['choice']
    correctAnswer = session['correctAnswer']
    if selectedAnswer == correctAnswer:
        isAnswerCorrect = True
        score = score+1
        session['score'] = score 
    else:
        isAnswerCorrect = False 
    
    total_num_of_test_questions = 3
    if count < total_num_of_test_questions:
        
        isLastQuestion = True if (count == total_num_of_test_questions-1) else False
        
        return render_template('result.html', isAnswerCorrect = isAnswerCorrect, selectedAnswer = selectedAnswer, correctAnswer= correctAnswer, score=score, count = count , isLastQuestion = isLastQuestion)
    else:
        return render_template('final_score.html', score=score, count = count)


@app.route('/finalresult', methods = ['POST'])
def finalresult():
    #check the answer
     
    return render_template('certificate.html')
   # return render_template('result.html', isAnswerCorrect = isAnswerCorrect, selectedAnswer = selectedAnswer, correctAnswer= correctAnswer)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        error_msg = ""  
        if username != "" and password != "":
            user = User.query.filter_by(username=username).first()
            if not user:
                error_msg = "Username does not exist"
                return render_template('login.html', error_msg=error_msg)
            elif user and user.password == password:
                session['username'] = username
                flash("LOGGED IN")
                return redirect('/')
            elif user and user.password != password:
                error_msg = "Incorrect Password"
                return render_template('login.html', error_msg=error_msg)

        else:
            error_msg = "Username and password cannot be blank"
            return render_template('login.html',error_msg=error_msg)
    else:
        return render_template("login.html")

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username=str.strip(request.form["username"])
        password=str.strip(request.form["password"])
        verify=str.strip(request.form["verify"])
    
        error_msg = ""

        if username != "" and password != "" and verify != "":
            if password != verify:
                error_msg = "Password and Verify password do not match"
                return render_template('signup.html', error_msg=error_msg)

            if len(username) < 3 or len(password) < 3:
                error_msg = "Username and Password should be atleast 3 character long"
                return render_template('signup.html', error_msg=error_msg)

            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/')
            else:
                error_msg = "User already exist"
                return render_template('signup.html', error_msg=error_msg)

        else:
            error_msg = "Please enter valid username, password and verify password"
            return render_template('signup.html', error_msg=error_msg)
    else: 
        return render_template('signup.html')

@app.route('/logout', methods = ['GET'])
def logout():
    del session['questionIdList']
    del session['correctAnswer']
    del session['grade']
    del session['subject']
    del session['score']
    del session['count']
    #del session['username']
    return redirect('/login')

if __name__ == '__main__':
    app.run()
