/* The deployed API. Left empty, the page talks to a local API on
   127.0.0.1:8787, which is how the Build It path runs. */
window.PAKKA_API = "https://t3ezfzhv5jh7qacktlcizc7hwy0mzodw.lambda-url.ap-south-1.on.aws";

/* The Telegram bot's handle, without the @. Left empty, the page says the bot
   is not configured rather than linking somewhere that does not exist. */
window.PAKKA_TELEGRAM = "pakka_check_bot";

/* WhatsApp, through Twilio's sandbox. The sandbox only answers numbers that
   have sent it the join code first, so the button sends that message for you.
   Left empty, the page says WhatsApp is not configured rather than sending
   someone to a number that will ignore them. */
window.PAKKA_WHATSAPP = { number: "14155238886", join: "join flow-double" };
