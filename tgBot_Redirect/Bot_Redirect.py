import telebot
import requests

token = "1313409276:AAF0fiE27nNGNgD1tG5KlD5wlLRYQlXTYHA"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def hello(message):
	bot.send_message(message.chat.id, "Hello, please insert a URL, which you wnat to check")

@bot.message_handler(content_types=['text'])
def redirect(message):
	try:
		r = requests.get(message.text)
		if r.history:
			mass = []
			for resp in r.history:
				mass.append(resp.url)
			text = ""
			count = 0
			while count < len(mass):
				if count + 1 < len(mass):
					text += mass[count] + '\n And then to:'
				else:
					text += mass[count]
				count += 1

			bot.send_message(message.chat.id, 'Request was redirected to: \n %s' %(text) + "\n Final destination: " + r.url)
		else:
			bot.send_message(message.chat.id, 'Request was not redirected')
	except requests.exceptions.MissingSchema:
			bot.send_message(message.chat.id, 'Invalid URL or URL is not found: \"%s\" \n Please insert corect URL' % (message.text))
	except requests.exceptions.InvalidSchema:
			bot.send_message(message.chat.id, 'Invalid URL or URL is not found: \"%s\" \n Please insert corect URL' % (message.text))

bot.polling()