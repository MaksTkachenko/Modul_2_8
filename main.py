import logging
from datetime import datetime, timedelta
# import datetime

import time
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes

TOKEN_BOT = "6624761473:AAHSarWlGYBMro_RHS6oOyuWYspoxEP84b8"


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

list_categories = ['food', 'transport', 'entertainment']

"""-------------------------------------work with data--------------------------------------"""
locale_time_now = time.localtime()
current_date = datetime.now().date()

time_string = time.strftime("%H:%M:%S, %Y-%m-%d", locale_time_now)

# data_now = time.strftime("%d/%m/%Y")
# data_string = time.strftime("%d-%m-%Y", locale_time_now)
# time_string_file = time.strftime("%d/%m/%Y-%d/%m")

# Знаходимо перший та останній день поточного тижня
current_week_start = current_date - timedelta(days=current_date.weekday())
current_week_end = current_week_start + timedelta(days=6)

# Визначаємо початок поточного місяця
current_month_start = current_date.replace(day=1)
# Знаходимо кінець поточного місяця
next_month = current_date.replace(day=28) + timedelta(days=4)  # Додаємо 4 дні, щоб впевнитися, що ми в межах місяця
current_month_end = next_month - timedelta(days=next_month.day)
"""------------------------------------------------------------------------------------------"""

FILENAME = "input_data_user.txt"
# FILENAME = "data_user.txt"

# re_exp_inc = r'(\d+): \[(\d+)\] - (\d{2}:\d{2}:\d{2}), (\d{2}-\d{2}-\d{4}) - \'(income|expense)\' - (\w+) - (\d+)'
re_exp_inc = r'(\d+): \[(\d+)\] - (\d{2}:\d{2}:\d{2}), (\d{4}-\d{2}-\d{2}) - \'(income|expense)\' - (\w+) - (\d+)'


class FinanceTracker:

    def __init__(self, time_now, exp_inc, categories, amount):
        self.exp_inc = exp_inc
        self.categories = categories
        self.amount = amount
        self.time_now = time_now

    def __str__(self):
        income = '➕'
        expense = '➖'

        if self.exp_inc == 'income':
            return f'{income} {self.categories} {self.amount}: {time_string}'
        if self.exp_inc == 'expense':
            return f'{expense} {self.categories} {self.amount}$: {time_string}'


"""------------------------------------------------------------------------------------------------------------------"""


def fun_check_user_id(user_id):

    with open(FILENAME, 'r') as file:

        for line in file:
            match = re.match(re_exp_inc, line)

            if match:
                group2 = match.group(2)

                if int(group2) == user_id:
                    return user_id

            '''if match is None:
                return False

            if match:
                group2 = match.group(2)

            list_id_user.append(int(group2))

        match value:
            case 1:
                for id_1 in list_id_user:
                    if id_1 == user_id:
                        return user_id

            case _:
                return "Incorrect number"'''


def fun_write_data_file(us_id, time_write, exp_inc, categories_write, suma_write):

    data_to_append = {f"[{us_id}] - {time_write} - '{exp_inc}' - {categories_write} - {suma_write}"}

    with open(FILENAME, 'r') as file:
        lines = file.readlines()

    last_index = int(lines[-1].split(':')[0]) if lines else 0

    # Додаємо нові дані з використанням останнього індексу + 1
    with open(FILENAME, 'a') as file:
        for line in data_to_append:
            last_index += 1
            file.write(f"{last_index}: {line}\n")


'''def fun_read_data_file(us_id, time_write, exp_inc, categories_write, suma_write):

    with open(input_FILE, "a") as file:
        file.write(f"[{us_id}] - {time_write} - '{exp_inc}' - {categories_write} - {suma_write}\n")

    with open(input_FILE, 'r') as input_file, open(FILENAME, 'w') as output_file:
        line_number = 1
        for line in input_file:
            output_file.write(f"{line_number}: {line}")
            line_number += 1'''


def fun_read_data_file(period: str, cat_exp_inc: str, categories: str, data: str):

    with open(FILENAME, 'r') as file:

        list_for_data = []
        total = 0

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

            match period:
                case "day":
                    if cat_exp_inc == group5 and categories == group6 and data == group4:
                        total += int(group7)

                        list_for_data.append(f'{group1} {group3} - {group4} - {group5} - {group6} - {group7}')
                        result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])

                case "month":
                    data_index_group = str(group4.split(' '))
                    parts_group = data_index_group.split("-")[1]

                    data_index = str(data.split(' '))
                    parts = data_index.split("-")[1]

                    if parts_group == parts:
                        if cat_exp_inc == group5 and categories == group6:
                            total += int(group7)

                            list_for_data.append(f'{group1} {group3} - {group4} - {group5} - {group6} - {group7}')
                            result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])
                case "year":

                    data_index_group = str(group4.split(' '))
                    parts_group = data_index_group.split("-")[0]

                    data_index = str(data.split(' '))
                    parts = data_index.split("-")[0]

                    if parts_group == parts:
                        if cat_exp_inc == group5 and categories == group6:
                            total += int(group7)

                            list_for_data.append(f'{group1} {group3} - {group4} - {group5} - {group6} - {group7}')
                            result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])

    return f"{result}\n\nTotal: {total}"


async def start(update: Update, context: CallbackContext) -> None:
    logging.info('Command "/start" was triggered')
    await update.message.reply_text("Welcome to my Wallet_Watch_Bot")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    logging.info('Command "/help_command" was triggered')

    await update.message.reply_text("Use /start to test this bot.")


async def show_categories(update: Update, context: CallbackContext) -> None:
    logging.info('Command "/show_categories" was triggered')
    category_list = "\n".join(list_categories)
    await update.message.reply_text(f"Доступні категорії:\n\n{category_list}")


async def start_add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    user_message = " ".join(context.args).split("|")
    categories = user_message[0].strip()
    suma = user_message[1].strip()

    if categories not in list_categories:
        await update.message.reply_text("Ви ввели не вірну категорію!!!")
        return
    if not suma.isdigit():
        await update.message.reply_text("Ви ввели не цифри!!!")
        return

    else:
        finance_tracker = FinanceTracker(time_string, 'expense', categories, suma)
        fun_write_data_file(user_id, time_string, 'expense', categories, suma)

    await update.message.reply_text(f"{finance_tracker} Successful")


async def start_add_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    user_message = " ".join(context.args).split("|")
    categories = user_message[0].strip()
    suma = user_message[1].strip()

    if not suma.isdigit():
        await update.message.reply_text("Ви ввели не цифри!!!")
        return

    finance_tracker = FinanceTracker(time_string, 'income', categories, suma)
    fun_write_data_file(user_id, time_string, 'income', categories, suma)

    await update.message.reply_text(f"{finance_tracker} Successful")


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

                if group5 == 'income' and int(group2) == user_id:
                    list_for_data.append(f'{int(group1)} - {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join(list_for_data)

    await update.message.reply_text(result)


async def view_all_transactions(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    logging.info('Command "/view_all_transactions" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
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
                group1 = match.group(1)  # Group 1: 2
                group2 = match.group(2)  # Group 2: 444238872
                group4 = match.group(4)  # Group 4: 26/08/2023
                group5 = match.group(5)  # Group 5: income/expense
                group6 = match.group(6)  # Group 6: ['food', 'transport', 'entertainment']
                group7 = match.group(7)  # Group 7: 9642

                line_date = datetime.strptime(group4, "%Y-%m-%d").date()

                if group5 == 'expense' and int(group2) == user_id and current_week_start <= line_date <= current_week_end:
                    total += int(group7)
                    list_for_data.append(f'{int(group1)}: {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join(list_for_data)

    await update.message.reply_text(f"All_transactions week:\n{result}\n\nTotal: {total}")


async def view_expenses_by_month(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/view_expenses_by_month" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    list_for_data = []
    total = 0
    with open(FILENAME, 'r') as file:

        for line in file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)  # Group 1: 2
                group2 = match.group(2)  # Group 2: 444238872
                group4 = match.group(4)  # Group 4: 26/08/2023
                group5 = match.group(5)  # Group 5: income/expense
                group6 = match.group(6)  # Group 6: ['food', 'transport', 'entertainment']
                group7 = match.group(7)  # Group 7: 9642

                line_date = datetime.strptime(group4, "%Y-%m-%d").date()

                if group5 == 'expense' and int(group2) == user_id and current_month_start <= line_date <= current_month_end:
                    total += int(group7)
                    list_for_data.append(f'{int(group1)}: {group6} - {group7}')

        for _ in list_for_data:
            result = '\n'.join(list_for_data)

    await update.message.reply_text(f"All_transactions month:\n{result}\n\nTotal: {total}")


async def statistics(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/statistics" was triggered')

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    user_message = " ".join(context.args).split("|")
    period = user_message[0].strip()
    cat_exp_inc = user_message[1].strip()
    categories = user_message[2].strip()
    data = user_message[3].strip()

    df = fun_read_data_file(period, cat_exp_inc, categories, data)

    await update.message.reply_text(df)


async def remove_expense(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/remove_expense" was triggered')

    removed_idx = int(context.args[0])

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    with open(FILENAME, 'r') as file:

        text_file = file.readlines()

        for line in text_file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)
                group2 = match.group(2)
                group5 = match.group(5)

                if group5 == 'expense' and int(group2) == user_id:
                    if int(group1) == removed_idx:
                        del text_file[removed_idx - 1]
                        break
                    if int(group1) > removed_idx:
                        await update.message.reply_text(f"You have entered an invalid index!!!")
                        return

    with open(FILENAME, 'w') as file_2:
        file_2.writelines(text_file)

    await update.message.reply_text(f"EXPENSE successfully removed")


async def remove_income(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/remove_income" was triggered')

    removed_idx = int(context.args[0])

    if fun_check_user_id(user_id) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    with open(FILENAME, 'r') as file:
        text_file = file.readlines()
        for line in text_file:
            match = re.match(re_exp_inc, line)
            if match:
                group1 = match.group(1)
                group2 = match.group(2)
                group5 = match.group(5)

                if group5 == 'income' and int(group2) == user_id:
                    if int(group1) == removed_idx:
                        del text_file[removed_idx - 1]
                        break
                    if int(group1) > removed_idx:
                        await update.message.reply_text(f"You have entered an invalid index!!!")
                        return

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
    app.add_handler(CommandHandler("view_transactions_week", view_expenses_by_week))
    app.add_handler(CommandHandler("view_transactions_month", view_expenses_by_month))
    app.add_handler(CommandHandler("statistics", statistics))


    app.run_polling()


if __name__ == "__main__":
    run()
