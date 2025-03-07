import telebot
import random

# Токен отримуємо від BotFather
API_TOKEN = '7736415415:AAHIbgoG8eiYiL096c9QKEJJohUkg-VKg6w'
bot = telebot.TeleBot(API_TOKEN)

class ZolotyiDoshCasinoBot:
    def __init__(self, balance=100):
        self.balance = balance
        self.ticket_price = 1
        self.numbers_range = 36
        self.num_choices = 5

    def buy_ticket(self, ticket):
        if self.balance >= self.ticket_price:
            self.balance -= self.ticket_price
            return ticket
        else:
            return None

    def draw_numbers(self):
        draw = random.sample(range(1, self.numbers_range + 1), self.num_choices)
        return draw

    def check_winnings(self, ticket, draw):
        matches = len(set(ticket).intersection(draw))

        if matches == 3:
            win = random.randint(10, 100)
        elif matches == 4:
            win = random.randint(10, 1000)
        elif matches == 5:
            win = random.randint(1000, 10000)
        else:
            win = 0

        self.balance += win
        return win

    def get_balance(self):
        return self.balance

# Створення об'єкта бота
user_bots = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_bots[message.chat.id] = ZolotyiDoshCasinoBot()
    bot.send_message(message.chat.id, "Вітаємо в ЗолотийДощКазино! Ваш стартовий баланс: 100. Для початку введіть /play")

@bot.message_handler(commands=['play'])
def play(message):
    user = message.chat.id
    if user not in user_bots:
        bot.send_message(user, "Спершу використайте команду /start для початку гри.")
        return

    bot.send_message(user, "Будь ласка, введіть ваш білет (5 чисел від 1 до 36, через пробіл):")
    bot.register_next_step_handler(message, process_ticket)

def process_ticket(message):
    user = message.chat.id
    ticket_str = message.text
    try:
        ticket = [int(x) for x in ticket_str.split()]
        if len(ticket) != 5 or any(x < 1 or x > 36 for x in ticket):
            bot.send_message(user, "Неправильний формат білета. Введіть 5 чисел від 1 до 36.")
            return
    except ValueError:
        bot.send_message(user, "Будь ласка, введіть лише числа.")
        return

    bot.send_message(user, f"Ваш білет: {ticket}")
    casino_bot = user_bots[user]
    draw = casino_bot.draw_numbers()
    bot.send_message(user, f"Розіграш: {draw}")

    win = casino_bot.check_winnings(ticket, draw)
    balance = casino_bot.get_balance()

    if win > 0:
        bot.send_message(user, f"Ви виграли {win}! Ваш новий баланс: {balance}")
    else:
        # Знімаємо 1 одиницю, якщо не виграли
        casino_bot.balance -= 1
        bot.send_message(user, f"Нічого не виграли. Ваш баланс: {balance - 1}")

# Обробник команд /balance для перевірки балансу
@bot.message_handler(commands=['balance'])
def balance(message):
    user = message.chat.id
    if user not in user_bots:
        bot.send_message(user, "Спершу використайте команду /start для початку гри.")
        return

    balance = user_bots[user].get_balance()
    bot.send_message(user, f"Ваш баланс: {balance}")

# Запуск бота з використанням polling
bot.polling(none_stop=True, interval=0)
