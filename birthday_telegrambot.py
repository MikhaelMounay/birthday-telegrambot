import telegram.ext
import datetime

def upcoming_birthdays(request_type):
  # Type the birthdays you want the Bot to remind you with below
  birthdays_dict = {
    "30/12": "Name"
  }
  today = f"{datetime.datetime.now().day}/{datetime.datetime.now().month}"

  if request_type == "today":
    upnext_day = f"{datetime.datetime.now().day + 1}/{datetime.datetime.now().month}"

    if (upnext_day in birthdays_dict):
      return f"{birthdays_dict[upnext_day]}'s birthday is on {today} 😊"
  
  elif request_type == "upcoming":
    day = datetime.datetime.now().day + 1
    month = datetime.datetime.now().month
    while True:
      tested_day = f"{day}/{month}"
      if (tested_day in birthdays_dict):
        return f"Closest Upcoming Birthday :\n\n{birthdays_dict[tested_day]}'s birthday is on {tested_day} 🤩"
      else:
        if day < 32:
          day += 1
        else:
          day = 1
          month += 1
  
  elif request_type == "thismonth":
    thismonth_birthdays = "This Month's Upcoming Birthdays (Total totalhere):"
    total = 0
    for i in range(1, 32):
      tested_day = f"{i}/{datetime.datetime.now().month}"
      if (tested_day in birthdays_dict):
        thismonth_birthdays += f"\n\n{birthdays_dict[tested_day]}'s birthday is on {tested_day} 🤩"
        total += 1
    thismonth_birthdays = thismonth_birthdays.replace("totalhere", str(total))
    return thismonth_birthdays

# Type your Telegram API Key Here
API_KEY = ""

def upcoming(update, context):
  update.message.reply_text(upcoming_birthdays("upcoming"))

def thismonth(update, context):
  update.message.reply_text(upcoming_birthdays("thismonth"))

def callback_birthday(context):
  context.bot.send_message(context.job.context, text=upcoming_birthdays("today"))

def birthday(update, context):
  context.job_queue.run_daily(callback_birthday, datetime.time(21, 0, 0), context=update.message.chat_id)

updater = telegram.ext.Updater(API_KEY, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", birthday))
disp.add_handler(telegram.ext.CommandHandler("upcoming", upcoming))
disp.add_handler(telegram.ext.CommandHandler("thismonth", thismonth))

updater.start_polling()
updater.idle()
