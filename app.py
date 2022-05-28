from email.policy import default
from http.client import REQUEST_URI_TOO_LONG
from winreg import REG_RESOURCE_LIST
from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

###################--- Application  Variable---#####################


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///survey.db'
db = SQLAlchemy(app)


### DATABASE
# 1 --->  Agreed  
# 2----> Neutral
# 3 ----> Disagree
class Respond(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Qn1 = db.Column(db.Integer,nullable = False ,default = 2)
    Qn2 = db.Column(db.Integer,nullable = False ,default = 2)
    Qn3 = db.Column(db.Integer,nullable = False ,default = 2)
    dateCreated = db.Column(db.DateTime,nullable = False ,default = datetime.utcnow)

    def __repr__(self):
        return f"Respond('{self.id}','{self.Qn1}','{self.Qn2}','{self.Qn3}','{self.dateCreated}')"





###################--- Application route---#####################


##----Home route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Guide')
def guide():
    return render_template('guide.html')

@app.route('/data/<int:Qn1>/<int:Qn2>/<int:Qn3>')
def send_data_responses(Qn1 ,Qn2 , Qn3):
    responseQn1 = Qn1
    responseQn2 = Qn2
    responseQn3 = Qn3

    newInstance = Respond(Qn1 = responseQn1 , Qn2 = responseQn2,Qn3 = responseQn3)
    try:
            db.session.add(newInstance)
            db.session.commit()
            return 'SuccessfulAdded'
    except:
            return "NotAdded"
     

##----Respondance route
@app.route('/survey-record')
def survey_record():
    #queryResponse = Respond.query.all()
    AgreedResponseQn1 = Respond.query.filter(Respond.Qn1 == 1).all()
    No_AgreedResponseQn1 = len(AgreedResponseQn1)

    AgreedResponseQn2 = Respond.query.filter(Respond.Qn2 == 1).all()
    No_AgreedResponseQn2 = len(AgreedResponseQn2)

    AgreedResponseQn3 = Respond.query.filter(Respond.Qn3 == 1).all()
    No_AgreedResponseQn3 = len(AgreedResponseQn3)

    sum1 = No_AgreedResponseQn1 + No_AgreedResponseQn2 + No_AgreedResponseQn3
    perc_agr_1 =percent(No_AgreedResponseQn1,sum1)
    perc_agr_2 =percent(No_AgreedResponseQn2,sum1)
    perc_agr_3 =percent(No_AgreedResponseQn3,sum1)
  
#--------------------------------------------------------------------------------
    NeutralResponseQn1 = Respond.query.filter(Respond.Qn1 == 2).all()
    No_NeutralResponseQn1 = len(NeutralResponseQn1)

    NeutralResponseQn2 = Respond.query.filter(Respond.Qn2 == 2).all()
    No_NeutralResponseQn2 = len(NeutralResponseQn2)

    NeutralResponseQn3 = Respond.query.filter(Respond.Qn3 == 2).all()
    No_NeutralResponseQn3 = len(NeutralResponseQn3)

    sum2 = No_NeutralResponseQn1 + No_NeutralResponseQn2 + No_NeutralResponseQn3
    perc_neu_1 =percent(No_NeutralResponseQn1,sum2)
    perc_neu_2 =percent(No_NeutralResponseQn2,sum2)
    perc_neu_3 =percent(No_NeutralResponseQn3,sum2)
  
    #--------------------------------------------------------------------------------
    DisagreedResponseQn1 = Respond.query.filter(Respond.Qn1 == 3).all()
    No_DisagreedResponseQn1 = len(DisagreedResponseQn1)

    DisagreedResponseQn2 = Respond.query.filter(Respond.Qn2 == 3).all()
    No_DisagreedResponseQn2 = len(DisagreedResponseQn2)

    DisagreedResponseQn3 = Respond.query.filter(Respond.Qn3 == 3).all()
    No_DisagreedResponseQn3 = len(DisagreedResponseQn3)

    sum3 = No_NeutralResponseQn1 + No_NeutralResponseQn2 + No_NeutralResponseQn3
    perc_dis_1 =percent(No_DisagreedResponseQn1,sum3)
    perc_dis_2 =percent(No_DisagreedResponseQn2,sum3)
    perc_dis_3 =percent(No_DisagreedResponseQn3,sum3)
#----------------------------------return------------------------------------------------
    return render_template('survey_record.html', No_AgreedResponseQn1 = No_AgreedResponseQn1 ,
    No_AgreedResponseQn2 = No_AgreedResponseQn2, 
    No_AgreedResponseQn3 =No_AgreedResponseQn3,
    No_NeutralResponseQn1 =No_NeutralResponseQn1,
    No_NeutralResponseQn2 =No_NeutralResponseQn2, 
    No_NeutralResponseQn3 = No_NeutralResponseQn3,
    No_DisagreedResponseQn1 =No_DisagreedResponseQn1,
    No_DisagreedResponseQn2 = No_DisagreedResponseQn2, 
    No_DisagreedResponseQn3 = No_DisagreedResponseQn3,
    perc_agr_1 =perc_agr_1,
    perc_agr_2 = perc_agr_2,
    perc_agr_3 = perc_agr_3,
    perc_neu_1 = perc_neu_1,
    perc_neu_2 = perc_neu_2,
    perc_neu_3 = perc_neu_3,
    perc_dis_1 = perc_dis_1,
    perc_dis_2 = perc_dis_2,
    perc_dis_3 = perc_dis_3)
    
def percent(upper,sum):
    result = (upper/sum)*100
    result = int(result)
    return result
#------------------------------------------------------

if __name__ == "__main__":
    app.run(debug = True)