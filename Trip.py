from Users import User
import yaml
import os
import markups

class Trip:
    trip_detail = {}

    def __init__(self, trip_id, trip_name, destination, state, start_date, end_date):
        self.trip_id = trip_id
        self.trip_name = trip_name
        self.destination = destination
        self.state = state
        self.start_date = start_date
        self.end_date = end_date
        self.users = []

        # Automatically create trip_details when a new instance is created
        with open('datahouse/trip.yaml', 'r') as f:
            self.trip_data = yaml.safe_load(f)

        if os.path.getsize('datahouse/trip.yaml') != 0:
            if self.trip_id not in self.trip_data.keys():
                Trip.trip_detail[trip_id] = {
                    'Trip name': self.trip_name,
                    'Destination': self.destination,
                    'State': self.state,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'User_id': []
                }
                new_trip = Trip.trip_detail
                with open('datahouse/trip.yaml', 'r') as f:
                    trips = yaml.safe_load(f)
                trips.update(new_trip)
                with open('datahouse/trip.yaml', 'w') as f:
                    yaml.dump(trips, f)
                # Update expenses with the new trip ID
                try:
                    with open('datahouse/expenses.yaml', 'r') as file:
                        expenses = yaml.safe_load(file) or {}

                    expenses[trip_id] = {}

                    with open('datahouse/expenses.yaml', 'w') as file:
                        yaml.safe_dump(expenses, file)
                except FileNotFoundError:
                    print("Expense file not found.")
            else:
                print('Trip with ID {} already exists in the database.'.format(self.trip_id))
        else:
            Trip.trip_detail[trip_id] = {
                'Trip name': self.trip_name,
                'Destination': self.destination,
                'State': self.state,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'User_id': []
            }
            new_trip = Trip.trip_detail
            with open('datahouse/trip.yaml', 'w') as f:
                yaml.dump(new_trip, f)
            print('No trip data found. Created a new trip with ID {}.'.format(self.trip_id))

        
        
    
    @classmethod    
    def add_user_to_trip(cls, trip_id, user_id):
        # Check if user_id exists in users.yaml
        with open('datahouse/users.yaml', 'r') as file:
            users = yaml.safe_load(file)
        
        if user_id in users:
            # Check if there is content present in trip.yaml file
            with open('datahouse/trip.yaml', 'r') as f:
                trips = yaml.safe_load(f)
            
            if trips and trip_id in trips.keys():
                trip_user_list = trips[trip_id]['User_id']
                
                if user_id not in trip_user_list:
                # add condition here
                    trips[trip_id]['User_id'].append(user_id)
                    with open('datahouse/trip.yaml', 'w') as f:
                        yaml.dump(trips, f)
                    back_button = "<br>< a href='/' class = 'button'>Go to Home</a>"
                    message =  'User with ID {} has been added into trip {}'.format(user_id,trip_id)
                    return message
                else:
                    return 'User {} already in your trip {}'.format(user_id,trip_id)
            else:
                return 'Sorry, the trip does not exist in your database'
        else:
            return 'Please registerd with userid {}  before joining/Creating a new trip'.format(user_id)
        
        
        
    @classmethod
    def delete_trip(cla, trip_id):
        
        # check if trip_id presents in trip yaml file
        with open('datahouse/trip.yaml','r') as f:
            trip_to_be_delted = yaml.safe_load(f)
        if trip_id in trip_to_be_delted.keys():
            trip_to_be_delted.pop(trip_id)
            with open('datahouse/trip.yaml','w') as f:
                yaml.dump(trip_to_be_delted,f)
            return 'Trip with ID {} has been deleted'.format(trip_id)
    
    @classmethod
    def trip_details(cls, trip_id):
        with open('datahouse/trip.yaml','r') as f:
            trips = yaml.safe_load(f)
        if trip_id in trips.keys():
            return trips[trip_id]
        
        # it will show the trips in UI will take care later
        
        
    # There will a button on ui for get user details(that page will be inside the)
    def show_all_users_from_a_Trip(self,trip_id_number):
        # will do UI time
        for trip_ids, trip_information in Trip.trip_detail.items():
            if trip_ids == trip_id_number:
                return Trip.trip_detail[trip_id_number]['User_id']
        return 'No group of trip is found with this trip ID {}'.format(trip_id_number)
    
    