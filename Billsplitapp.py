import yaml

class BillSplit:
    @staticmethod
    def calculate_final_amount(trip_id):
        expenses = BillSplit.load_expenses()
        trip_expenses = expenses.get(trip_id, {})
        
        if not trip_expenses:
            return "Trip not found or has no expenses."
        
        users = list(trip_expenses.keys())
        bills = list(trip_expenses.values())
        
        total_amount = sum(bills)
        individual_sum = total_amount / len(users)
        
        settled_amounts = {}
        for i in range(len(users)):
            settled_amounts[users[i]] = int(bills[i] - individual_sum)
            
        return settled_amounts
            

    @staticmethod
    def load_expenses():
        try:
            with open('datahouse/expenses.yaml', 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return {}

    @staticmethod
    def load_users():
        try:
            with open('datahouse/users.yaml', 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return {}

