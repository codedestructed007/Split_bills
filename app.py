import os
from flask import Flask, render_template, request,flash,redirect,url_for
from markupsafe import Markup
from flask import session
import yaml

from Users import User
from Trip import Trip
from Expense import Expense
from Billsplitapp import BillSplit
from Basic_Utility import Bais_utility

#paths
users_path = 'datahouse/users.yaml'
trip_path = 'datahouse/trip.yaml'
expense_path = 'datahouse/expenses.yaml'


app = Flask(__name__)
app.secret_key = 'KYMT1223'

@app.route('/',methods=['GET'])
def home_page():
    return render_template('home.html')


@app.route('/already_registered')
def check_registered_user():
    # render to page to take userid
    return render_template('already_registered.html')


@app.route('/process_user',methods=['GET','POST'])
def processing_user():
    registered_users = Bais_utility.load_yaml_file(users_path)
    if request.method == 'POST':
        user_id = request.form['user_id']
        session['user_id'] = user_id
        if user_id in registered_users.keys():
            # check if this user_id is in any trip group
            trips = Bais_utility.load_yaml_file(trip_path)
            user_name = registered_users[user_id]['name']
            
            # condition if user id is registered with
            return render_template('trip_check_page.html',user_name =user_name)
        else:
            # go and register yourself first
            flash('Sorry, no user ID {} is registerd with us.'.format(user_id))
            return render_template('register_with_userid.html')
    else:
        return render_template('register_with_userid.html')
    
    
@app.route('/trips_page',methods=['POST','GET'])
def trip_page():
    trip_file = Bais_utility.load_yaml_file(trip_path)
    users_file = Bais_utility.load_yaml_file(users_path)
    
    
    if request.method == 'POST':    # post method
        
        trip_id = request.form['trip_id']
        if trip_id in trip_file.keys() :
            trip_details  = trip_file[trip_id]
            user_id_list = trip_details.get('User_id',[])
            users_with_id = {}
            for user_id in user_id_list:
                users_with_id[user_id]=users_file.get(user_id,{}).get('name','Name not found')
            #user_details
            return render_template('trips.html',trip_details = trip_details,users_with_id = users_with_id,trip_id = trip_id)
        else:
            print('this is get method and it is working')
            # go add yourself into the trip

            return render_template('already_registered.html')
    else:
        
        return render_template('trips.html')
    
    
@app.route('/user_registration',methods=['GET','POST'])
def user_registration():
    if request.method == 'POST':
        name = request.form['name']
        session['name'] = name
        id = request.form['user_id']
        email = request.form['email']
        session['email'] = email
        # load data 
        users = Bais_utility.load_yaml_file(users_path)
        #update data
        user_details = {}
        user_details[id] = {
            'email' : email,
            'name' : name
        }
        users.update(user_details)
        #dump data
        Bais_utility.dump_into_yaml_file(users_path,users)
        return redirect(url_for('home_page'))
    # else if method is GET
    else:
        return redirect(url_for('processing_user'))

@app.route('/all_available_trips',methods=['GET','POST'])
def all_trips(message=None):
    print('hels')
    all_trips = Bais_utility.load_yaml_file(trip_path)
    users = Bais_utility.load_yaml_file(users_path)
    return render_template('all_trips.html',trips= all_trips,users=users,message = message)

@app.route('/expenses_page')
def expenses_page():
    trip_id = request.args.get('trip_id')
    expenses = Bais_utility.load_yaml_file(expense_path)
    users = Bais_utility.load_yaml_file(users_path)
    bills = {}
    bills = expenses[trip_id]
    return render_template('expenses.html', bills = bills, users=users, trip_id=trip_id)

@app.route('/add_share_page')
def add_share():
    trip_id = request.args.get('trip_id')
    expences = Bais_utility.load_yaml_file(expense_path)
    return render_template('add_your_share.html',trip_id=trip_id,expences = expences)
    



@app.route('/add_me_into_trip')
def add_into_trip():
    trip_id=  request.args.get('trip_id')
    #return to already_registerd
    return render_template('register_user_to_trip_id.html',trip_id=trip_id)

@app.route('/adding_user_into_trip/<trip_id>', methods=['POST'])
def add_user_to_trip(trip_id):
    if request.method == 'POST':
        user_id = request.form['user_id']
        registered_users = Bais_utility.load_yaml_file(users_path)
        
        message = Trip.add_user_to_trip(trip_id=trip_id,user_id=user_id)        
        # user_name = registered_users[user_id]['name']
        # now update expense yaml file with showing 0 amount to new user
        if message == 'User with ID {} has been added into trip {}'.format(user_id,trip_id):
            expenses=Bais_utility.load_yaml_file(expense_path)
            new_user = {}
            new_user[user_id] = 0
            expenses[trip_id].update(new_user)
            Bais_utility.dump_into_yaml_file(expense_path,expenses)
        return message

    # Handle other cases if needed
    return render_template('register_user_to_trip_id.html')




@app.route('/delete_member_from_trip')
def delete_trip_member():
    trip_id= request.args.get('trip_id')
    trip_dictionary=Trip.trip_details(trip_id=trip_id)
    return render_template('delete_members.html',trip_id=trip_id,trip_dictionary=trip_dictionary)

@app.route('/delete_member_from_trip/<trip_id>', methods=['GET', 'POST'])
def delete_member_from_trip(trip_id):
    trip_members = Bais_utility.load_yaml_file(trip_path)
    user_id_to_be_deleted = request.form['user_id']
    if trip_id in trip_members:
            # Check if the user_id exists in the list of User_ids
            if user_id_to_be_deleted in trip_members[trip_id]['User_id']:
                # Remove the user_id_to_be_deleted from the list
                trip_members[trip_id]['User_id'].remove(user_id_to_be_deleted)
                
                # Save the modified data back to the YAML file
                Bais_utility.dump_into_yaml_file(trip_path, trip_members)
                return render_template('home.html')
            else:
                return f"User {user_id_to_be_deleted} not found in trip {trip_id}"
            
    else:
        return f"Trip {trip_id} not found"
    
    
    
    
@app.route('/submit_share/<trip_id>', methods=['POST','GET'])
def submit_share(trip_id):
    print('working1')
    if request.method == 'POST':
        print('working2')
        user_id = request.form['user_id']
        amount = float(request.form['amount'])

        # Load existing expenses data
        expenses = Bais_utility.load_yaml_file(expense_path)

        # Check if the user_id exists in expenses
        if trip_id in expenses:
            print('working3')
            if user_id in expenses[trip_id].keys():
            # Update the existing user's share amount
                expenses[trip_id][user_id] += amount
                Bais_utility.dump_into_yaml_file(expense_path,expenses)
                flash(f'Amount {amount} has been recorded')
                print('if first')
                return redirect(url_for('submit_share', trip_id=trip_id))
            else:
                print('else1')
                return redirect(url_for('add_into_trip',trip_id=trip_id))
        else:
            # Redirect logic to add user to trip
            # For example:
            # return redirect(url_for('add_user_to_trip', user_id=user_id))
            pass
        # Update the expenses YAML file with the modified data

        return f"Share of {amount} added for user {user_id} in trip {trip_id}."
    else:
        # this is get method
        expences = Bais_utility.load_yaml_file(expense_path)
        return redirect(url_for('add_share',trip_id=trip_id,expences = expences))




@app.route('/create_new_trip', methods = ['GET','POST'])
def new_trip_page():
    return render_template('new_trip_page.html')

@app.route('/create_trip', methods=['POST'])
def create_trip():
    if request.method == 'POST':
        # Retrieve form data
        trip_id = request.form.get('trip_id')
        trip_name = request.form.get('trip_name')
        destination = request.form.get('destination')
        state = request.form.get('state')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        user_id = request.form.get('user_id')

        # Create a new trip instance
        new_trip = Trip(trip_id, trip_name, destination, state, start_date, end_date)

        # Add the user to the newly created trip
    

        message= f'Your trip with ID {trip_id} has been created!'
        
        all_trips = Bais_utility.load_yaml_file(trip_path)
        users = Bais_utility.load_yaml_file(users_path)
        return redirect(url_for('all_trips',trips=all_trips, users=users,message=message))



@app.route('/registered_users')
def registered_users():
    # Access the show_all_registered_users method from Users class
    users = User.show_all_registered_users()

    # Render the HTML template with registered users
    return render_template('registered_users.html', users=users)





@app.route('/show_final_amounts', methods=['GET', 'POST'])
def final_amount_page():
    trip_id = request.args.get('trip_id')
    users = Bais_utility.load_yaml_file(users_path)
    if trip_id is None:
        return "No trip ID provided."

    final_amount = BillSplit.calculate_final_amount(trip_id=trip_id)
    
    if final_amount:
        return render_template('settled_up_page.html', final_amount=final_amount,users=users,trip_id=trip_id)
    else:
        return "No final amount calculated for this trip."


@app.route('/settle_bill')
def reset_user_amounts():
    try:
        
        # trip_id
        trip_id = request.args.get('trip_id')
        # Load the YAML data
        data= Bais_utility.load_yaml_file(expense_path)
        
        if data and trip_id in data:
            # Reset amounts to zero for the specified trip_id
            data[trip_id] = {user_id: 0 for user_id in data[trip_id].keys()}
        
            # Save the modified data back to the file
            Bais_utility.dump_into_yaml_file(expense_path,data)
            success_message = 'Successfully settled all bills! Thanks for using our service'
            home_button = "<br><a href='/' class='button'>Go to Home</a>"
            return  Markup(success_message + home_page)
    
        else:
            return 'Trip_id not found'  # Trip_id not found or empty data
        
    except FileNotFoundError:
        return 'File not found or empty'  # File not found or empty
            
@app.route('/routing_to_trips',methods=['GET','POST']) 
def route_to_trip():
    trip_id = request.args.get('trip_id')
    trip_file = Bais_utility.load_yaml_file(trip_path)
    users_file = Bais_utility.load_yaml_file(users_path)
    
    if trip_id in trip_file.keys():
        trip_details = trip_file[trip_id]
        user_id_list = trip_details.get('User_id',[])
        users_with_id = {}
        for user_id in user_id_list:
            users_with_id[user_id] = users_file.get(user_id,{}).get('name','Name not found')
            
        return render_template('trips.html',trip_details = trip_details,users_with_id = users_with_id,trip_id = trip_id)
            



if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)




