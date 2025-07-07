import time
import schedule
from birthday_bot import run_bot
from telegram_alert import check_for_command, init_telegram_updates

schedule.every().day.at("14:00").do(run_bot)   # 7:30 PM IST
schedule.every().day.at("23:30").do(run_bot)  # 6:30 PM EST (Canada)
schedule.every().day.at("00:00").do(run_bot)  # 7:00 PM EST (USA)


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
