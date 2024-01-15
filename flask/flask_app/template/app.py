#flaskアプリ構築用ライブラリ
from flask import Flask, render_template,request
from wtforms import Form, TextAreaField,  FloatField, IntegerField,SubmitField, \
   validatorsfrom, validators, ValidationError
#機械学習に必要なライブラリ
import pickle
import os
from sklearn.metrics import r2_score
import pandas as pd

#学習済みモデルの読み込み
def predict(parameters):
    model = pickle.load(open(os.path.join('regressor.pkl'),'rb'))
    params = parameters.
    pred=model.predict(params)
    return pred

app = Flask(__name__)
app.config.form_object(__name__)
app.config['SECRET_KEY'] = 'eaogjajjadjjaigiaha1230r4'



class FeatureNameForm(Form):
    modelyear = FloatField('モデル年(年)',
                           [validators.InputRequired("この項目は入力必須です。"),
                            validators.NumberRange(min=0,max=2023)])
    color = '赤'
    mileage = FloatField('走行距離(km)',
                         default=0)
    guarantee_period = FloatField('保証年(年)',default=0)
    displacement = FloatField('排気量(cc)',
                              [validators.InputRequired("この項目は入力必須です。"),
                               validators.NumberRange(min=0,max=3000)])
    type = 'スポーツ/ツアラー'
    brand = 'HONDA'

    #html側で表示する予想ボタンの表示
    submit = SubmitField('予想')

@app.route('/',methods =['GET','POS'])