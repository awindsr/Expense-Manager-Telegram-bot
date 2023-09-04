import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib

# Set up Google Sheets credentials
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# Get the sheet by title
sheet = client.open('Expense Manager').sheet1

# Get the list of authorized users from credential.py module
from credential import AUTHORIZED_USERS

def is_user_authorized(user_id):
    """
    Check if the user is authorized to interact with the bot
    """
    return user_id in AUTHORIZED_USERS

def get_category_index(category):
    """
    Get the index of the category in the sheet
    """
    categories = sheet.row_values(1)
    if category in categories:
        return categories.index(category) + 1
    else:
        # Add a new category if it doesn't exist
        category_index = len(categories) + 1
        sheet.update_cell(1, category_index, category)
        return category_index

def add_expense(category, month, amount):
    """
    Add the expense to the sheet
    """
    # Get the column index for the month
    month_index = sheet.row_values(1).index(month + '-' + str(datetime.datetime.now().year)) + 1
    if month_index == 0:
        # Month not found
        return 'Invalid month'

    # Get the row index for the category
    category_index = get_category_index(category)

    # Add the amount to the cell
    cell_value = sheet.cell(category_index, month_index).value
    if cell_value == '':
        sheet.update_cell(category_index, month_index, amount)
    else:
        sheet.update_cell(category_index, month_index, float(cell_value) + float(amount))
    return 'Expense added successfully'

def delete_expense(category, month, amount):
    """
    Delete the expense from the sheet
    """
    # Get the column index for the month
    month_index = sheet.row_values(1).index(month + '-' + str(datetime.datetime.now().year)) + 1
    if month_index == 0:
        # Month not found
        return 'Invalid month'

    # Get the row index for the category
    category_index = get_category_index(category)

    # Subtract the amount from the cell
    cell_value = sheet.cell(category_index, month_index).value
    if cell_value == '':
        return 'No expense found'
    else:
        new_value = float(cell_value) - float(amount)
        if new_value < 0:
            new_value = 0
        sheet.update_cell(category_index, month_index, new_value)
        return 'Expense deleted successfully'

def generate_summary(from_date=None, to_date=None):
    if from_date and to_date:
        from_date = datetime.strptime(from_date, "%d%m%y").date()
        to_date = datetime.strptime(to_date, "%d%m%y").date()
        if to_date < from_date:
            return "Invalid date range! Please enter a valid date range."
        values = sheet.get_all_values()
        header_row = values[0]
        data_rows = values[1:]
        category_index = header_row.index("Category")
        month_indexes = {}
        for month_col in header_row[1:]:
            try:
                date = datetime.strptime(month_col, "%B %Y").date()
                if from_date <= date <= to_date:
                    month_indexes[month_col] = header_row.index(month_col)
            except ValueError:
                continue
        if not month_indexes:
            return "No data found for the specified date range!"
        category_expense_map = {}
        for data_row in data_rows:
            category = data_row[category_index]
            if category not in category_expense_map:
                category_expense_map[category] = 0
            for month, month_index in month_indexes.items():
                if data_row[month_index]:
                    expense = float(data_row[month_index])
                    category_expense_map[category] += expense
        total_expense = sum(category_expense_map.values())
        if not total_expense:
            return "No data found for the specified date range!"
        labels = list(category_expense_map.keys())
        values = list(category_expense_map.values())
        fig = plt.figure(figsize=(5, 5))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title(f"Expense Summary from {from_date.strftime('%d/%m/%Y')} to {to_date.strftime('%d/%m/%Y')}")
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return buf
    else:
        month = from_date
        month_index = get_month_index(month)
        if month_index is None:
            return f"No data found for {month}"
        expenses = get_expenses_by_month(sheet, month_index)
        if not expenses:
            return f"No data found for {month}"
        category_expense_map = {}
        for expense in expenses:
            category = expense.category
            if category not in category_expense_map:
                category_expense_map[category] = 0
            category_expense_map[category] += expense.amount
        total_expense = sum(category_expense_map.values())
        if not total_expense:
            return f"No data found for {month}"
        labels = list(category_expense_map.keys())
        values = list(category_expense_map.values())
        fig = plt.figure(figsize=(5, 5))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title(f"Expense Summary for {month}")
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        return buf
