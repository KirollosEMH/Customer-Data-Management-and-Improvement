import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle

# Create flask app
flask_app = Flask(__name__)

# Load the scaler and model
review_model = pickle.load(open("model_review.pkl", "rb"))
churn_model = pickle.load(open("model_churn.pkl", "rb"))

dataset = pd.read_csv("dataset_features_v1-5.csv")

@flask_app.route("/")
def Home():
    return render_template("index.html")

@flask_app.route("/predict", methods=["POST"])
def predict():
    # Get form data
    input_data = [str(x) for x in request.form.values()]
    
    
    prediction_type = request.form.get("prediction_type")
    
    columns = ['order_id', 'customer_id', 'order_item_id', 'product_id', 
               'seller_id', 'customer_unique_id', 'review_id']
    
    input_data = pd.DataFrame([input_data[:-1]], columns=columns)
    input_data['order_item_id'] = int(input_data['order_item_id'])

    X = pd.merge(input_data, dataset, on=columns, how='inner').head(1)

    X = X.drop(columns=columns)
    if prediction_type == "review":
        X = X.drop(columns=['review_score'])

        prediction = review_model.predict(X)
        if prediction == 1:
            prediction = "Score 1"
        elif prediction == 2:
            prediction = "Score 2"
        elif prediction == 3:
            prediction = "Score 3"
        elif prediction == 4:
            prediction = "Score 4"
        elif prediction == 5:
            prediction = "Score 5"
        return render_template("index.html", prediction_text="The predicted output is {}".format(prediction))
    elif prediction_type == "churn":
        X = X.drop(columns=['churn'])
        prediction = churn_model.predict(X)
        if prediction == 0:
            prediction = "Not Churned"
        elif prediction == 1:
            prediction = "Churned"
        return render_template("index.html", prediction_text="The predicted output is {}".format(prediction))

if __name__ == "__main__":
    flask_app.run(debug=True, port=8080)
