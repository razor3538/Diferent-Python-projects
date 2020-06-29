import telebot
import requests

token = "1313409276:AAF0fiE27nNGNgD1tG5KlD5wlLRYQlXTYHA"

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def redirect(message):
	try:
		r = requests.get(message.text)
		if r.history:
			bot.send_message(message.chat.id, 'Request was redirected')
			for resp in r.history:
				bot.send_message(message.chat.id, 'Status code: ' + str(resp.status_code) + '\n' + resp.url)
			bot.send_message(message.chat.id, 'Final destination: \n' + 'Status code: ' + str(r.status_code) + '\n' + r.url)
		else:
			bot.send_message(message.chat.id, 'Request was not redirected')
	except requests.exceptions.MissingSchema:
		bot.send_message(message.chat.id, 'Invalid URL or URL is not found: \"%s\" \n Please insert corect URL' % (message.text))


bot.polling()
