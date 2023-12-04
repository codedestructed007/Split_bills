import yaml

class Expense:
    @staticmethod
    def add_expense(trip_id, user_id, amount):
        if Expense.is_valid_trip(trip_id):
            if Expense.is_valid_user_in_trip(trip_id, user_id):
                expenses = Expense.load_expenses()
                trip_expenses = expenses.get(trip_id, {})
                user_expenses = trip_expenses.get(user_id, 0)
                user_expenses += amount
                trip_expenses[user_id] = user_expenses
                expenses[trip_id] = trip_expenses
                Expense.save_expenses(expenses)
            else:
                print(f"User '{user_id}' is not a member of the trip '{trip_id}'.")
        else:
            print(f"Trip with ID '{trip_id}' does not exist.")

    @staticmethod
    def is_valid_trip(trip_id):
        with open('datahouse/trip.yaml', 'r') as file:
            trips = yaml.safe_load(file) or {}
            return trip_id in trips
    @staticmethod
    def get_total_expenses(trip_id):
        expenses = Expense.load_expenses()
        return expenses.get(trip_id, {})
    
    @staticmethod
    def is_valid_user_in_trip(trip_id, user_id):
        with open('datahouse/trip.yaml', 'r') as file:
            trips = yaml.safe_load(file) or {}
            if trip_id in trips:
                return user_id in trips[trip_id].get('User_id', [])
            return False
    @staticmethod
    def load_expenses():
        try:
            with open('datahouse/expenses.yaml', 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return 'File Not found'
   
    @staticmethod
    def save_expenses(expenses):
        with open('datahouse/expenses.yaml', 'w') as file:
            yaml.dump(expenses, file)


