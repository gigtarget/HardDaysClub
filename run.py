import time
import schedule
from birthday_bot import run_bot
from telegram_alert import check_for_command, init_telegram_updates

schedule.every().day.at("09:00").do(run_bot)
schedule.every().day.at("12:00").do(run_bot)
schedule.every().day.at("18:00").do(run_bot)
schedule.every().day.at("21:00").do(run_bot)


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
