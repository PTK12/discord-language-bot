# discord-language-bot
A discord bot that tests users on their language (currently Spanish - vocab list sourced from AQA GCSE).

**NOTICE: This bot is unlikely to be updated in the future**
If there's activity or people are interested, I may consider working on this project again.

# About

There are currently 3 commands to test yourself.

## q
Format: **q** [list] - do 1 multiple choice from [list]

Pick the correct Spanish term within 5 seconds.

## quiz
Format: **quiz** [list] [20] - do [20] multiple choice questions from [list]

Perform as many multiple choice questions (same as q command). Getting 3 wrong will stop the quiz.

## spell
Format: **spell** [list] [1] - do [1] spelling sessions from [list]

Translate the term from English to Spanish within 10 seconds. Your next message will be tested.

# Other

If you'd like to use a vocab list other than the one provided (e.g. French), format as below:
```json
{
  "Topic 1": [["French", "English"], ...],  
  "Topic 2": [...],
  ...
}
```

 # TODO
- Cleaning up code (linting, type hinting, ...)
- Better language import system
- Add slash commands
- Host an official 24/7 bot on server
