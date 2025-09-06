from flask import Flask, request, render_template
import pandas as pd
from networksecurity.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


## Route for landing page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
    SFH = int(request.form.get('SFH')),
    popUpWidnow = int(request.form.get('popUpWidnow')),
    SSLfinal_State = int(request.form.get('SSLfinal_State')),
    Request_URL = int(request.form.get('Request_URL')),
    URL_of_Anchor = int(request.form.get('URL_of_Anchor')),
    web_traffic = int(request.form.get('web_traffic')),
    URL_Length = int(request.form.get('URL_Length')),
    age_of_domain = int(request.form.get('age_of_domain')),
    having_IP_Address = int(request.form.get('having_IP_Address'))
)

        pred_df = data.get_data_as_data_frame()
        print("User Input:", pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        prediction = "🚨 Malicious Website" if results[0] == 1 else "✅ Safe Website"

        return render_template('home.html', results=prediction)


if __name__ == "__main__":
    app.run(debug=True)
