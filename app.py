import sqlite3
import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', monthly_fee=None)

@app.route('/', methods=['POST'])
def submit():                          

    db_path = os.path.join(os.path.dirname(__file__), 'attendance.db') 

    if not os.path.exists(db_path):
        return render_template('index.html', monthly_fee="DB not found")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    def query_fee_breakdown(regime_code, scenario_code):
        
        lookup_code = regime_code + '_' + scenario_code
        cursor.execute("SELECT F1, F2, F3, F4, Monthly_Fee, Weekly_fee FROM StoredCalculationResults WHERE key = ?", (lookup_code,))
        extract = cursor.fetchone()
        
        return extract

    child_age = int(request.form.get('child_age', 0))  

    if child_age > 6 or child_age < 0:
        return "Invalid age", 400
    
    funded_hours = int(request.form.get('funding_status', 0))

    valid_funding_hours = {0, 15, 30}
    if funded_hours not in valid_funding_hours:
        return render_template('index.html', monthly_fee="Invalid funding hours")
    
    days = request.form.get('days', "0")                                         
    am_hours = request.form.get('morning_sessions', "0")
    pm_hours = request.form.get('afternoon_sessions', "0")

    params = [days, am_hours, pm_hours]
    params = [p if p else "0" for p in params]
    
    i = 0

    for i in range(len(params)):
        if params[i] == "":
            params[i] = "0"
        if int(params[i]) > 5 or int(params[i]) < 0: 
            return "Age out of range", 400 

    regime = None 
            
    if (child_age >= 0 and child_age < 2):
        match funded_hours:
            case 0:
                regime = 'ST_under2'
            case 15:
                regime = 'G_02_15'
            case 30:
                regime = 'G_02_30'
    elif (child_age >= 2 and child_age < 3):
        match funded_hours:
            case 0:
                regime = 'ST_2_to_3'
            case 15:
                regime = 'G_23_15'
            case 30:
                regime = 'G_23_30' 
    elif (child_age >= 3 and child_age <= 6):
        match funded_hours:
            case 0:
                regime = 'ST_over3'
            case 15:
                regime = 'G_35_15'
            case 30:
                regime = 'G_35_30'                      
                                                                        
    sce_code = params[0] + '_' + params[1] + '_' + params[2] 

    extract = query_fee_breakdown(regime, sce_code)
   
    cursor.close()
    connection.close()

    output = [x for x in extract]                                                                                                                    

    if extract: 
        monthly_fee = output[4]
        funded_hours_wk = output[0]
        extras_cost = output[1]
        hours_added = output[2]
        unfunded_hours_cost = output[3]
    else:
        monthly_fee = 0
        funded_hours_wk = 0
        extras_cost = 0
        hours_added = 0
        unfunded_hours_cost = 0

    return render_template('index.html', monthly_fee = monthly_fee, funded_hours_wk = funded_hours_wk , extras_cost = extras_cost, hours_added = hours_added, unfunded_hours_cost = unfunded_hours_cost)

if __name__== '__main__':
    app.run()





