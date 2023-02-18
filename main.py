from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def gpt(promt):
  import openai
  a = promt
  openai.api_key = "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"
  response = openai.Completion.create(
    model="text-davinci-001",
    prompt=a,
    temperature=0.4,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  ans = response['choices'][0]['text']
  return ans




app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'



db = SQLAlchemy(app)
class Feedback(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), nullable=False)
  role = db.Column(db.String(250))
  feedback = db.Column(db.String(2500))
  datetime = db.Column(db.DateTime, default=datetime.utcnow)





@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    find = request.form["find"]
    breakFast = gpt(f"act as my dietition and tell me about any one breakfast for a person preparing a diet plan for {find} it should be brief and under 50 words")
    lunch = gpt(f"act as my dietition and tell me about any one lunch for a person preparing a diet plan for {find} it should be brief and under 50 words")
    dinner = gpt(f"act as my dietition and tell me about any one dinner for a person preparing a diet plan for {find} it should be brief and under 50 words")
    return render_template("diet.html", diet={"breakFast": breakFast, "lunch": lunch, "dinner": dinner})
  return render_template("index.html", name="index")

@app.route('/feedbacks')
def feedbacks():
  feedbacks = Feedback.query.all()
  return render_template("feedbacks.html", name="feedbacks", feedbacks=feedbacks)


@app.route('/feedback', methods=["GET", "POST"])
def feedback():
  if request.method == "POST":
    name = request.form['name']
    role = request.form['role']
    feedback = request.form['feedback']
    db.session.add(Feedback(name=name, role=role, feedback=feedback))
    db.session.commit()
    return redirect("feedbacks")
  return render_template("feedback.html", name="feedback")

@app.route('/feedbackdel', methods=["GET", "POST"])
def feedbackdel():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    if username == "hadimabroor" and password == "Mabroor@123":
      feedbacks = Feedback.query.all()
      return render_template("feedbackdel.html", name="feedbacks", feedbacks=feedbacks)
    else:
      return redirect("feedbacks")
  else:
    return render_template("login.html")

@app.route('/del')
def delete():
  if request.method == "POST":
    id = request.form['id']
    feedback = db.get_or_404(Feedback, id)
    db.session.delete(feedback)
    db.session.commit()
  else:
    return redirect("/")
  



app.run(host='0.0.0.0', port=81)

