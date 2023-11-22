from flask import Flask, request, render_template, flash, redirect
from flask import session, make_response
from flask_debugtoolbar import DebugToolbarExtension
# from survey import * // I don't know what to import yet...
from surveys import surveys as SURVEYS

app = Flask(__name__)

# enabling the toolbar
app.debug = True
app.config["SECRET_KEY"] = "secret-key"
toolbar = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False # disabling DEBUG_TB_INTERCEPT_REDIRECTS

question_number = 0 # question user is currently on

# routes
@app.route('/')
def show_home():
    """renders homepage, shows list of surveys"""
    global question_number
    
    question_number = 0
    # session["RESPONSES"] = [] # keep track of user responses
    return render_template("homepage.html", surveys=SURVEYS, q_num=question_number)

@app.route(f'/survey/<survey_id>/question/<int:question_number>')
def show_survey(survey_id, question_number):
    """creates a webpage with the question from the survey you started"""
    if survey_id in SURVEYS:
        
        lengthOfSurvey = len(SURVEYS[survey_id].questions) - 1
        lengthOfResponses = len(session["RESPONSES"])

        if(question_number > lengthOfResponses):
            flash("Invalid question!")
            return redirect(f"/survey/{survey_id}/question/{lengthOfResponses}?") # should take you to last question you answered

        title = SURVEYS[survey_id].title
        question = SURVEYS[survey_id].questions # these are a array (list) of 'Question' objects
        choices = SURVEYS[survey_id].questions[question_number].choices

        
        return render_template('question_base.html', title=title, questions=question[question_number], choices=choices, q_num=question_number, survey_id=survey_id)
    else:
        flash("Survey doesn't exist")
        return redirect('/');

@app.route('/survey/<survey_id>/POST_REPONSE')
def post_reponses(survey_id):
    """Gets user choice, appends to REPONSES, updates question number and redirects user to next question"""
    global question_number
    
    lengthOfSurvey = len(SURVEYS[survey_id].questions)
    
    if(question_number >= lengthOfSurvey-1): # "Survey is completed" run before we get 'index_out_of_bounds'
        
        choice = request.args["choice"]
        
        # creates a copy of session["RESPONSES"] appends choice to the copy and copies over session["RESPONSES"]
        RESPONSES = session["RESPONSES"]
        RESPONSES.append(choice)
        session["RESPONSES"] = RESPONSES

        question_number = 0
        return redirect(f"/survey/{survey_id}/completed_form")
    else:
        choice = request.args["choice"]
        
        RESPONSES = session["RESPONSES"]
        RESPONSES.append(choice)
        session["RESPONSES"] = RESPONSES
        question_number += 1

        return redirect(f"/survey/{survey_id}/question/{question_number}?")

@app.route("/survey/<survey_id>/completed_form")
def show_completed_form(survey_id):
    return render_template("completed_form.html")
