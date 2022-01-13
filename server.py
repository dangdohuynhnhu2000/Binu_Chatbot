from flask import Flask, request, jsonify, render_template
import pickle
from pyvi import ViTokenizer
from sklearn.feature_extraction.text import CountVectorizer
import json
import random
from weather import Get_Weather, Get_Temp, prov_data
from covid import Get_Covid_Data
import os

f = open('data/Data.json', encoding="utf-8")
data = json.load(f)
f.close()

d = dict()
for obj in data:
    if 'responses' in obj.keys():
        d[obj['tag']] = obj['responses']

app = Flask(__name__)
with open('model.pkl', 'rb') as model_f:
    vect, model = pickle.load(model_f)

ask_user = False #đánh dấu việc chatbot có hỏi lại thông tin không
domain = "" #lưu lại chủ đề

def preprocess(sent):
    punct = [',', '.', '!', '?']
    sent = sent.lower()
    tokens = ViTokenizer.tokenize(sent)
    tokens = tokens.split()
    for t in tokens:
        if t in punct:
            tokens.remove(t)
    return ' '.join(tokens)


@app.route('/')
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response(): 
    global ask_user
    global domain 
    msg = request.form["msg"]
    question = preprocess(msg)

    X_test = vect.transform([question])
    prob = model.predict_proba(X_test)
    max_prob = prob[0].max(axis=0)
    tag_pred = model.predict(X_test)

    if max_prob <= 0.5:
        if ask_user == False:
            return "Mình không hiểu bạn nói gì."
        else:
            #dự đoán lại câu hỏi trong trường hợp người dùng input loại câu hỏi khác
            if domain == "weather":    
                ask_user, res =  Get_Weather(prov_data, question)
                return res
            elif domain == "temp":
                ask_user, res = Get_Temp(prov_data, question)
                return res

    domain = tag_pred #lưu lại cho trường hợp chatbot cần hỏi lại thông tin từ user

    if ask_user == True:
        if domain == "weather":    
            ask_user, res =  Get_Weather(prov_data, question)
            return res
        elif domain == "temp":
            ask_user, res = Get_Temp(prov_data, question)
            return res

    #câu hỏi về covid
    if tag_pred == "covid_general":
        return Get_Covid_Data(question, 4)
    elif tag_pred == "cases_yesterday":
        return Get_Covid_Data(question, 0)
    elif tag_pred == "total_cases":
        return Get_Covid_Data(question, 1)
    elif tag_pred == "deaths_yesterday":
        return Get_Covid_Data(question, 2)
    elif tag_pred == "total_deaths":
        return Get_Covid_Data(question, 3)

    #câu hỏi về thời tiết, nhiệt độ
    if tag_pred == "weather":    
        ask_user, res =  Get_Weather(prov_data, question)
        return res
    elif tag_pred == "temp":
        ask_user, res = Get_Temp(prov_data, question)
        return res
    
    #câu hỏi có sẵn câu trả lời trong dữ liệu
    res = random.choice(d[tag_pred[0]])
    return res
if __name__ == '__main__':
    app.run(port=5000)