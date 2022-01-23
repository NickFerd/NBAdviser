# NBAdviser
Recommender telegram bot of NBA games   
https://t.me/nbadviser_bot  
Made with python-telegram-bot and nba_api libraries

## Intentions
Can't watch NBA game live? Want to find an interesting and intense game without discovering the final score?  
NBAdviser's goal is to help with that.

## Setup
Clone the repo. There is a docker-compose file to get the bot going.  
Of course, it needs a token for startup. Create an .env txt file with the following structure in the same directory where docker-compose file is.
```
NBADVISER_TOKEN=<your_token>
NBADVISER_CONTROL_CHAT_ID=<chat_id>
```
Control chat id is optional to get messages in telegram if errors happens.

Then simply run:  
`docker-compose up -d`

