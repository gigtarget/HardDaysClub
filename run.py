import time
import schedule
from birthday_bot import run_bot
from telegram_alert import check_for_command, init_telegram_updates

# Schedule one daily post at 7:30 PM IST (14:00 UTC)
schedule.every().day.at("14:00").do(run_bot)

def main():
    init_telegram_updates()
    print("Bot ready. Send /run in Telegram to trigger.")
    while True:
        if check_for_command("/run"):
            run_bot()
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
