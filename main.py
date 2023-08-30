import logging
import datetime
import time
import re

from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes

TOKEN_BOT = "6624761473:AAHSarWlGYBMro_RHS6oOyuWYspoxEP84b8"

'''user_data_expense = dict()
user_data_income = dict()'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )

list_categories = ['food', 'transport', 'entertainment']

locale_time_now = time.localtime()
time_string = time.strftime("%H:%M:%S, %d/%m/%Y", locale_time_now)
time_string_file = time.strftime("%d/%m/%Y-%d/%m")

# input_FILE = "input_data_user.txt"
FILENAME = "data_user.txt"

re_exp_inc = r'(\d+): \[(\d+)\] - (\d{2}:\d{2}:\d{2}), (\d{2}/\d{2}/\d{4}) - \'(income|expense)\' - (\w+) - (\d+)'
re_exp_inc_1 = r'(\[(\d+)\] - (\d{2}:\d{2}:\d{2}), (\d{2}/\d{2}/\d{4}) - \'(income|expense)\' - (\w+) - (\d+)'


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


def fun_read_file(user_id, value=None):

    with open(FILENAME, 'r') as file:

        list_id_user = []

        for line in file:
            match = re.match(re_exp_inc, line)

            if match is None:
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
                return "Incorrect number"


def fun_read_data_file(us_id, time_write, exp_inc, categories_write, suma_write):

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
    else:
        finance_tracker = FinanceTracker(time_string, 'expense', categories, suma)
        # user_data_expense[user_id].append(finance_tracker)

        fun_read_data_file(user_id, time_string, 'expense', categories, suma)

    await update.message.reply_text(f"{finance_tracker} Successful")


async def start_add_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    user_message = " ".join(context.args).split("|")
    categories = user_message[0].strip()
    suma = user_message[1].strip()

    finance_tracker = FinanceTracker(time_string, 'income', categories, suma)
    # user_data_income[user_id].append(finance_tracker)

    fun_read_data_file(user_id, time_string, 'income', categories, suma)

    await update.message.reply_text(f"{finance_tracker} Successful")


async def show_added_expense(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/show_add_expense" was triggered')

    if fun_read_file(user_id, 1) != user_id:
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

    # result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])
    await update.message.reply_text(result)


async def show_added_income(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/show_add_income" was triggered')

    if fun_read_file(user_id, 1) != user_id:
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

    # result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(list_for_data)])
    await update.message.reply_text(result)


async def remove_expense(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    logging.info('Command "/remove_expense" was triggered')

    removed_idx = int(context.args[0])

    if fun_read_file(user_id, 1) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    with open(FILENAME, 'r') as file:

        text_file = file.readlines()
        count = 0
        for line in text_file:
            count += 1
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

    if fun_read_file(user_id, 1) != user_id:
        await update.message.reply_text("You don't have any expense to remove")
        return

    with open(FILENAME, 'r') as file:

        text_file = file.readlines()
        count = 0
        for line in text_file:
            count += 1
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
    app.add_handler(CommandHandler("show_added_expense", show_added_expense))
    app.add_handler(CommandHandler("show_added_income", show_added_income))
    app.add_handler(CommandHandler("remove_expense", remove_expense))
    app.add_handler(CommandHandler("remove_income", remove_income))

    app.run_polling()


if __name__ == "__main__":
    run()
