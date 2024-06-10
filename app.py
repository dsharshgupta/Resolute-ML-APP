from flask import Flask, render_template,request
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)
cluster_scaler = joblib.load('models/cluster_scaler.pkl')
class_scaler = joblib.load('models/class_scale.pkl')
pca = joblib.load('models/cluster_pca.pkl')
label = joblib.load('models/class_encoder.pkl')
kmeans = joblib.load('models/cluster_model.pkl')
Svm = joblib.load('models/class_model.pkl')
result = np.array(pd.read_csv(r"data/cluster_data.csv"))
data = pd.read_excel(r"data/rawdata.xlsx")

def calculate_position_duration(data, date):
    data['datetime'] = pd.to_datetime(data['date'].astype(str) + " " + data['time'].astype(str))
    data = data.sort_values(by='datetime')
    data['duration'] = data['datetime'].diff().shift(0)
    data = data[(data['date'] == date)]
    inside_duration = 0
    outside_duration = 0
    for i in range(data.shape[0] - 1):
        if str(data.iloc[i, 0])[0:10] == date:
            if data.iloc[i, 6] == 'inside':
                inside_duration += data.iloc[i + 1, 9].total_seconds()
            else:
                outside_duration += data.iloc[i + 1, 9].total_seconds()
    inside_duration_hours = int(inside_duration // 3600)
    inside_duration_minutes = int((inside_duration % 3600) // 60)
    outside_duration_hours = int(outside_duration // 3600)
    outside_duration_minutes = int((outside_duration % 3600) // 60)
    return (inside_duration_hours, inside_duration_minutes), (outside_duration_hours, outside_duration_minutes)
def duration_datewise(data):
    unique_dates = data['date'].unique()
    results = []
    for date in unique_dates:
        date = str(date)[0:10]
        inside_duration, outside_duration = calculate_position_duration(data, date)
        results.append((date, inside_duration, outside_duration))
    return results
def calculate_activity_number(data,date):
  data = data[(data['date']==date)]
  placed = 0
  picked = 0
  for _, row in data.iterrows():
    if row["activity"] == 'placed':
      placed+=1
    else:
      picked+=1
  return placed,picked
def activity_datewise(data):
  unique_dates = data['date'].unique()
  results = []
  for date in unique_dates:
    date = str(date)[0:10]
    placed,picked = calculate_activity_number(data,date)
    results.append((date,placed,picked))
  return results

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/cluster', methods=['GET','POST'])
def cluster():
    if request.method == 'POST':
        input_features = [float(request.form[f'feature{i+1}']) for i in range(18)]
        input_features = np.array(input_features).reshape(1, -1)
        scaled_features = cluster_scaler.transform(input_features)
        pca_features = pca.transform(scaled_features)
        predicted_cluster = kmeans.predict(pca_features)[0]
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=result[:, 1], y=result[:, 2], hue=result[:,3], palette='viridis')
        centers = kmeans.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], marker='x', color='red', s=150, label='Centers')
        plt.scatter(pca_features[:, 0], pca_features[:, 1], marker='o', color='blue', s=100, label='New Point')
        plt.title(f"The predicted class of the point is {predicted_cluster}")
        plt.legend()
        plt.savefig('static/result.png')
        plt.clf() 
        return render_template('cluster_result.html', cluster=predicted_cluster,centers=centers)
    return render_template('clustering.html')

@app.route('/classification',methods=['GET','POST'])
def classification():
    if request.method=='POST':
        input_features = [float(request.form[f'feature{i+1}']) for i in range(18)]
        input_features = np.array(input_features).reshape(1, -1)
        scaled_features = class_scaler.transform(input_features)
        predicted_class = Svm.predict(scaled_features)
        predicted_class = label.inverse_transform(predicted_class)[0]
        return render_template('classification_result.html',p_class=predicted_class)
    return render_template('classification.html')

@app.route('/python')
def python():
    duration_results = duration_datewise(data)
    activity_results = activity_datewise(data)
    return render_template('python.html', duration_results=duration_results, activity_results=activity_results)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080)