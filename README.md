# Modul_2_8

Створити ТГ бот для ведення доходів і витрат, бот повинен мати такий функціонал:

1. Мати можливість додавати витрати вказуючи категорію
2. Категорії повинні бути захардкожені у коді
3. Повертати список доступних категорій
4. Додавати доходи з вказанням категорії доходів, але тут не потрібно перевіряти, просто всі категорії приймайте
5. Можливість переглядати всі витрати, витрати за місяць та за тиждень.
6. Видаляти витрати або доходи
7. Дивитись статистику доходів витрат по категоріям за день, місяць, тиждень та рік

Зберігати дані потрібно у файлі, для того щоб після закінчення роботи програми у вас дані зберігались.


start - description of the bot
help - a list of commands and their use
categories - list of available categories
add_expense - command to add expenses
add_income - command to add income
remove_expense - command to remove expenses
remove_income - command to remove income
show_expense - show a list of all costs
show_income - show a list of all incomes
view_all_transactions - list of all transactions
view_expense_week - a list of all expenses for the current week
view_expense_month - a list of all expenses for the current month
statistics - a command for viewing income and expenditure statistics


List of commands and their use:

1. /start - description of the bot
2. /help - a list of commands and their use
3 /categories - list of available categories for expenses
4 /add_expense - command to add expenses (example of use: /add_expense food | 126)
5. /add_income - command to add income (usage example: /add_income work| 15000)
6. /remove_expense - command to remove expenses (use example: /remove_expense "line number") to view the /show_expense list
7. /remove_income - command to remove income (use example: /remove_income "line number") to view the /show_expense list
8. /show_expense - list of added expenses
9. /show_income - list of added incomes
10. /view_all_transactions - a list of all transactions
11. /view_expense_week - a list of all expenses for the current week
12. /view_expense_month - a list of all expenses for the current month
13. /statistics - a command for viewing income and expenditure statistics
usage example:
/statistics day | "income/expense" | "job/auto" | 2023-09-05
/statistics month | "income/expense" | "job/auto" | 2023-09-05
/statistics year | "income/expense" | "job/auto" | 2023-09-05