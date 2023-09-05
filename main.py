import logging
from datetime import datetime, timedelta

import time
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes

TOKEN_BOT = "6624761473:AAHSarWlGYBMro_RHS6oOyuWYspoxEP84b8"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

list_categories = ['transport', 'entertainment', 'auto', 'products', 'payments', 'household goods', 'other',
                   'restaurant', 'pharmacy', 'travel']

"""-------------------------------------work with data--------------------------------------"""
locale_time_now = time.localtime()  # current time
current_date = datetime.now().date()  # current date

time_string = time.strftime("%H:%M, %Y-%m-%d", locale_time_now)

# We find the first and last day of the current week
current_week_start = current_date - timedelta(days=current_date.weekday())
current_week_end = current_week_start + timedelta(days=6)

# We define the beginning of the current month
current_month_start = current_date.replace(day=1)

# We find the end of the current month
next_month = current_date.replace(day=28) + timedelta(days=4)  # Додаємо 4 дні, щоб впевнитися, що ми в межах місяця
current_month_end = next_month - timedelta(days=next_month.day)

FILENAME = "input_data_user.txt"

re_exp_inc = r'(\d+): \[(\d+)\] - (\d{2}:\d{2}), (\d{4}.\d{2}.\d{2}) - \'(income|expense)\' - (\w+) - (\d+)'


class FinanceTracker:

    def __init__(self, time_now, exp_inc, categories, amount):
        self.time_now = time_now
        self.exp_inc = exp_inc
        self.categories = categories
        self.amount = amount

    def __str__(self):
        income = '🤑'
        expense = '💸'

        if self.exp_inc == 'income':
            return (f'{income} Income from the category of "{self.categories}" in the amount '
                    f'of {self.amount} grn have been successfully added')

        if self.exp_inc == 'expense':
            return (f'{expense} Expenses from the category of "{self.categories}" in the amount '
                    f'of {self.amount} grn have been successfully added')


def fun_check_user_id(user_id):

    with open(FILENAME, 'r') as file:

        for line in file:
            match = re.match(re_exp_inc, line)

            if match:
                group2 = match.group(2)

                if int(group2) == user_id:
                    return user_id


def fun_write_data_file(us_id, time_write, exp_inc, categories_write, suma_write):

    data_to_append = {f"[{us_id}] - {time_write} - '{exp_inc}' - {categories_write} - {suma_write}"}

    with open(FILENAME, 'r') as file:
        lines = file.readlines()

    last_index = int(lines[-1].split(':')[0]) if lines else 0

    # We add new data using the last index +1
    with open(FILENAME, 'a') as file:
        for line in data_to_append:
            last_index += 1
            file.write(f"{last_index}: {line}\n")


def fun_read_data_file(period: str, cat_exp_inc: str, categories: str, data: str):

    with open(FILENAME, 'r') as file:

        list_for_data = []
        total = 0

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group3 = match.group(3)  # Group 3: 16:24:37
                group4 = match.group(4)  # Group 4: 26/08/2023
                group5 = match.group(5)  # Group 5: income/expense
                group6 = match.group(6)  # Group 6: ['food', 'transport', 'entertainment']
                group7 = match.group(7)  # Group 7: 9642

            match period:
                case "day":
                    if cat_exp_inc == group5 and categories == group6 and data == group4:
                        total += int(group7)

                        list_for_data.append(f'{group3} - {group4} - {group5} - {group6} - {group7}')
                        result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])

                case "month":
                    data_index_group = str(group4.split(' '))
                    parts_group = data_index_group.split("-")[1]

                    data_index = str(data.split(' '))
                    parts = data_index.split("-")[1]

                    if parts_group == parts:
                        if cat_exp_inc == group5 and categories == group6:
                            total += int(group7)

                            list_for_data.append(f'{group3} - {group4} - {group5} - {group6} - {group7}')
                            result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])
                case "year":

                    data_index_group = str(group4.split(' '))
                    parts_group = data_index_group.split("-")[0]

                    data_index = str(data.split(' '))
                    parts = data_index.split("-")[0]

                    if parts_group == parts:
                        if cat_exp_inc == group5 and categories == group6:
                            total += int(group7)

                            list_for_data.append(f'{group3} - {group4} - {group5} - {group6} - {group7}')
                            result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])

    if len(list_for_data) == 0:
        return f"No records found!!!"
    else:
        return f"{result}\n\nTotal: {total}"


def fun_available_remove_index(user_id, inc_exp: str, value=None):
    with open(FILENAME, 'r') as file:

        list_available_index_remove = []

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)  # Group 1: 2
                group2 = match.group(2)  # Group 2: 444238872
                group5 = match.group(5)  # Group 5: income/expense

            match value:
                case 1:
                    if user_id == int(group2) and inc_exp == group5:
                        list_available_index_remove.append(int(group1))
                case 2:
                    if user_id == int(group2) and str(inc_exp) == group5:
                        list_available_index_remove.append(int(group1))

    return list_available_index_remove


async def start(update: Update, context: CallbackContext) -> None:
    logging.info('Command "/start" was triggered')
    await update.message.reply_text("Welcome to Wallet_Watch_Bot\nThis bot was created to manage income and "
                                    "expenses.\n\n"
                                    "Functionality of the bot:\n"
                                    "1. the ability to add expenses by specifying a category\n"
                                    "2. Add income indicating the category of income\n"
                                    "3. The ability to review all expenses, expenses per month and per week.\n"
                                    "4. Delete expenses or income.\n"
                                    "5. View statistics of income and expenses by category for the day, month, "
                                    "week and year\n\nView a list of commands and how to use them /help")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    logging.info('Command "/help_command" was triggered')

    await update.message.reply_text("List of commands and their use:\n\n"
                                    "1. /start - description of the bot\n"
                                    "2. /help - a list of commands and their use\n"
                                    "3. /categories - list of available categories for expenses\n"
                                    "4. /add_expense - command to add expenses\n"
                                    "     (example of use: /add_expense auto | 126)\n"
                                    "5. /add_income - command to add income\n "
                                    "    (example of use: /add_income job| 15000)\n"
                                    "6. /remove_expense - command to remove expenses\n"
                                    "    (use example: /remove_expense 'line number')\n "
                                    "    to view the list /show_expense \n"
                                    "7. /remove_income - command to remove income\n"
                                    "    (use example: /remove_income 'line number')\n"
                                    "    to view the list /show_expense\n"
                                    "8. /show_expense - list of added expenses\n"
                                    "9. /show_income - list of added incomes\n"
                                    "10. /view_all_transactions - a list of all transactions\n"
                                    "11. /view_expense_week - a list of all expenses for the current\n"
                                    "       week\n"
                                    "12. /view_expense_month - a list of all expenses for the current\n"
                                    "       month\n"
                                    "13. /statistics - a command for viewing income and\n"
                                    "       expenditure statistics. Usage example:\n"
                                    "/statistics day | 'income/expense' | 'job/auto' | 2023-09-05\n"
                                    "/statistics month | 'income/expense' | 'job/auto' | 2023-09-05\n"
                                    "/statistics year | 'income/expense | 'job/auto' | 2023-09-05")


async def show_categories(update: Update, context: CallbackContext) -> None:
    logging.info('Command "/show_categories" was triggered')
    category_list = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_categories)])
    await update.message.reply_text(f"Available categories:\n\n{category_list}")


async def start_add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    user_message = " ".join(context.args).split("|")
    categories = user_message[0].strip()
    suma = user_message[1].strip()

    if categories not in list_categories:
        await update.message.reply_text("You have entered an incorrect category!!!")
        return

    if not suma.isdigit():
        await update.message.reply_text("You entered the wrong numbers!!!")
        return

    else:
        finance_tracker = FinanceTracker(time_string, 'expense', categories, suma)
        fun_write_data_file(user_id, time_string, 'expense', categories, suma)

    await update.message.reply_text(f"{finance_tracker}")


async def start_add_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    user_message = " ".join(context.args).split("|")
    categories = user_message[0].strip()
    suma = user_message[1].strip()

    if not suma.isdigit():
        await update.message.reply_text("You entered the wrong numbers!!!")
        return

    finance_tracker = FinanceTracker(time_string, 'income', categories, suma)
    fun_write_data_file(user_id, time_string, 'income', categories, suma)

    await update.message.reply_text(f"{finance_tracker}")


async def show_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/show_add_expense" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any EXPENSE records")
        return

    with open(FILENAME, 'r') as file:

        list_for_data = []

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)
                group2 = match.group(2)
                group5 = match.group(5)
                group6 = match.group(6)
                group7 = match.group(7)

                if group5 == 'expense' and int(group2) == user_id:
                    list_for_data.append(f'{int(group1)}: {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join(list_for_data)

    await update.message.reply_text(result)


async def show_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/show_add_income" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any INCOME records")
        return

    with open(FILENAME, 'r') as file:

        list_for_data = []

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)
                group2 = match.group(2)
                group5 = match.group(5)
                group6 = match.group(6)
                group7 = match.group(7)

                if group5 == 'income' and int(group2) == user_id:
                    list_for_data.append(f'{int(group1)} - {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join(list_for_data)

    await update.message.reply_text(result)


async def view_all_transactions(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    logging.info('Command "/view_all_transactions" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You have no records!!!")
        return

    with open(FILENAME, 'r') as file:

        list_for_data = []

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)  # Group 1: 2
                group2 = match.group(2)  # Group 2: 444238872
                group3 = match.group(3)  # Group 3: 16:24:37
                group4 = match.group(4)  # Group 4: 26/08/2023
                group5 = match.group(5)  # Group 5: income/expense
                group6 = match.group(6)  # Group 6: ['food', 'transport', 'entertainment']
                group7 = match.group(7)  # Group 7: 9642

                if int(group2) == user_id:
                    list_for_data.append(f'{int(group1)}: {group4} - {group3} - {group5} - {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join(list_for_data)

    await update.message.reply_text(f"All_transactions:\n{result}")


async def view_expenses_by_week(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/view_expenses_by_week" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    list_for_data = []
    total = 0
    with open(FILENAME, 'r') as file:

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group2 = match.group(2)  # Group 2: 444238872
                group3 = match.group(3)  # Group 3: 11:54:06
                group4 = match.group(4)  # Group 4: 26-08-2023
                group5 = match.group(5)  # Group 5: income/expense
                group6 = match.group(6)  # Group 6: ['food', 'transport', 'entertainment']
                group7 = match.group(7)  # Group 7: 9642

                line_date = datetime.strptime(group4, "%Y-%m-%d").date()

                if group5 == 'expense' and int(group2) == user_id and current_week_start <= line_date <= current_week_end:
                    total += int(group7)
                    list_for_data.append(f' {group3}  {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])

    await update.message.reply_text(f"All expenses per week:\n\n{result}\n\nTotal: {total}")


async def view_expenses_by_month(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/view_expenses_by_month" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You have no records!!!")
        return

    list_for_data = []
    total = 0
    with open(FILENAME, 'r') as file:

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group2 = match.group(2)
                group3 = match.group(3)
                group4 = match.group(4)
                group5 = match.group(5)
                group6 = match.group(6)
                group7 = match.group(7)

                line_date = datetime.strptime(group4, "%Y-%m-%d").date()

                if group5 == 'expense' and int(group2) == user_id and current_month_start <= line_date <= current_month_end:
                    total += int(group7)
                    list_for_data.append(f' {group3}  {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])

    await update.message.reply_text(f"All expenses per month:\n\n{result}\n\nTotal: {total}")


async def statistics(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/statistics" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You have no records!!!")
        return

    user_message = " ".join(context.args).split("|")
    period = user_message[0].strip()
    cat_exp_inc = user_message[1].strip()
    categories = user_message[2].strip()
    data = user_message[3].strip()

    list_data = fun_read_data_file(period, cat_exp_inc, categories, data)

    await update.message.reply_text(list_data)


async def remove_expense(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/remove_expense" was triggered')

    removed_idx = int(context.args[0])

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    user_input_index = int(update.message.text)

    comparison = fun_available_remove_index(user_id, 'expense', 1)

    if user_input_index not in comparison:
        await update.message.reply_text(f"You have entered an invalid index!!!")
        return

    with open(FILENAME, 'r') as file:

        text_file = file.readlines()
        line_count = 0
        for line in text_file:
            line_count += 1
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)
                group2 = match.group(2)
                group5 = match.group(5)

                if group5 == 'expense' and int(group2) == user_id:
                    if int(group1) == user_input_index:
                        del text_file[removed_idx - 1]
                        break

    with open(FILENAME, 'w') as file_2:
        file_2.writelines(text_file)

    await update.message.reply_text(f"EXPENSE successfully removed")


async def remove_income(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/remove_income" was triggered')

    removed_idx = int(context.args[0])

    comparison = fun_available_remove_index(user_id, 'expense', 1)

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    if removed_idx not in comparison:
        await update.message.reply_text(f"You have entered an invalid index!!!")
        return

    with open(FILENAME, 'r') as file:
        text_file = file.readlines()
        line_count = 0
        for line in text_file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)
                group2 = match.group(2)
                group5 = match.group(5)

                if group5 == 'income' and int(group2) == user_id:
                    if int(group1) == removed_idx:
                        del text_file[line_count - 1]
                        break

    with open(FILENAME, 'w') as file_2:
        file_2.writelines(text_file)

    await update.message.reply_text(f"INCOME successfully removed")


def run():
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    logging.info("Aplication build succesfully!")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("categories", show_categories))
    app.add_handler(CommandHandler("add_expense", start_add_expense))
    app.add_handler(CommandHandler("add_income", start_add_income))
    app.add_handler(CommandHandler("show_expense", show_expense))
    app.add_handler(CommandHandler("show_income", show_income))
    app.add_handler(CommandHandler("remove_expense", remove_expense))
    app.add_handler(CommandHandler("remove_income", remove_income))
    app.add_handler(CommandHandler("view_all_transactions", view_all_transactions))
    app.add_handler(CommandHandler("view_expense_week", view_expenses_by_week))
    app.add_handler(CommandHandler("view_expense_month", view_expenses_by_month))
    app.add_handler(CommandHandler("statistics", statistics))

    app.run_polling()


if __name__ == "__main__":
    run()
