import sqlite3
import os
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='F:\PremierPro\YT\VID006\Code')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():                           # try to link app code here

    db_path = os.path.join(os.path.dirname(__file__), 'attendance.db') 

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    def query_fee_breakdown(regime_code, scenario_code):
        
        lookup_code = regime_code + '_' + scenario_code
        cursor = connection.cursor()
        cursor.execute("SELECT F1, F2, F3, F4, Monthly_Fee, Weekly_fee FROM StoredCalculationResults WHERE key = ?", (lookup_code,))
        extract = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return extract

    days = request.form.get('days')                                         
    am_hours = request.form.get('morning_sessions')
    pm_hours = request.form.get('afternoon_sessions')

    params = [days, am_hours, pm_hours]

    i = 0

    for i in range(len(params)):
        if params[i] == "":
            params[i] = "0"
        if int(params[i]) > 5 or int(params[i]) < 0: 
            print("Value out of bounds, please enter session values between 1 and 5.")      # TODO look into input validation  chapt4er in AOTOMATE THE BORING STUFF BOOK P.190
            break
                
    child_age = requests.form.get('child_age')  ################ TODO MODIFY THIS FOR HTML FORM INPUT
    
    if child_age > 6 or child_age < 0:
        print('Invalid age, please enter age between 0 and 5')
        exit

    valid_funding_hours = {0, 15, 30}

    try:
        funded_hours = int(input("Enter a number (0, 15, or 30): "))
        if funded_hours in valid_funding_hours:                                ################  TODO MODIFY THIS FOR HTML FORM INPUT
            print(f"Accepted value: {funded_hours}")
                        
        else:
            print(" Invalid input. Please enter 0, 15, or 30.")
    except ValueError:
        print("Please enter a valid integer.")

        funding_status = input('Please enter funding status (type f/u funded /unfunded: )\n')

        if not (funding_status == 'f' or funding_status == 'u'):
            print('Invalid Entry')
            exit
                
        if (child_age >= 0 and child_age < 2):
            match funded_hours:
                case 0:
                    regime = 'ST_under2'
                case 15:
                    regime = 'G_02_15'
                case 30:
                    regime = 'G_02_30'
        if (child_age >= 2 and child_age < 3):
            match funded_hours:
                case 0:
                    regime = 'ST_2_to_3'
                case 15:
                    regime = 'G_23_15'
                case 30:
                    regime = 'G_23_30' 
        if (child_age >= 3 and child_age <= 6):
            match funded_hours:
                case 0:
                    regime = 'ST_over3'
                case 15:
                    regime = 'G_35_15'
                case 30:
                    regime = 'G_35_30'                      
                                                                        
    sce_code = params[0] + '_' + params[1] + '_' + params[2] 

    extract = query_fee_breakdown(regime, sce_code)

    output = [x for x in extract]                                                                                                                     # this section needs to be made into a function

    monthly_fee = output[4]

    return render_template('index.html', monthly_fee = monthly_fee)

if __name__== '__main__':
    app.run()




    #app.run(debug=True)
                
    # first_name = input('Please enter first name:\n')
    # last_name = input('Pleaes enter last name:\n')                # Be careful with spaces here as it feeds into the variable and the SQL query.

    # connection = sqlite3.connect(db_path)
    # cursor = connection.cursor()

    # cursor.execute("SELECT Latest_Invoice_Price, key1, RegimeKey FROM child_static WHERE LastName = ? AND FirstName = ?", (last_name, first_name))                
    # dbextract = cursor.fetchone()

    # out2 = dbextract

    # invoice_price = out2[0]
    # sce_code = out2[1]
    # reg_code = out2[2]
                
    # scenario_fee_component = query_fee_breakdown(reg_code,sce_code)
                
    # m2_output = [x for x in scenario_fee_component]

    # print(f'\nLatest Invoice Price is: £{invoice_price}')
    # print(f'\n ')
    # print(f'\nThe monthly fee for this combination is: £{m2_output[4]}')
    # print(f'\n         COST BREAKDOWN FOR THIS SCENARIO TYPE:')
    # print(f'\nThe Number of funded hours/week is: {m2_output[0]}')
    # print(f'\nThe Cost of extras and Food Supplemnet is: £{m2_output[1]}')
    # print(f'\nThe Number of hours added is: {m2_output[2]}')
    # print(f'\nThe cost of the unfunded hours is: £{m2_output[3]}')
                
    # cursor.close()
    # connection.close()






