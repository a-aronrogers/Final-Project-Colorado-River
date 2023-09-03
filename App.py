from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataretrieval import nwis
import pandas as pd
from sklearn.metrics import mean_squared_error

app = Flask(__name__)


df = pd.read_csv('./data/sites_info.csv',dtype={'site_no':str})
df_future = pd.read_csv('./data/future_data.csv',index_col=0)


@app.route('/', methods=['GET', 'POST'])
def index():
    
    result = None
    
    columns = [col for col in df_future.columns if len(col) == 8]
    
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        if user_input in df_future.columns:
            
            data = nwis.get_iv(sites=user_input)
            discharge = data[0]['00060'][0]
            date = data[0].index[0].strftime('%Y-%m-%d')

            predicted = df_future.loc[date,user_input]

            result = f'The actual discharge is {discharge},but the predicted is {int(predicted)} for {user_input}. That is {abs(discharge - int(predicted))} cubic feet per second off!'
            

    return render_template('index.html', result=result,columns=columns)

if __name__ == '__main__':
    app.run(debug=True)
