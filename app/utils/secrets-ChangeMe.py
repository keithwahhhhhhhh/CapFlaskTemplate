# The purpose of this file is to hold sensitive information that you don't want to 
# post publicly to GitHub.  This file is excluded from being sent to github by .gitignore

# For the email recovery using a gmail account to work you need to turn on "less secure apps" 
# here https://myaccount.google.com/lesssecureapps

def getSecrets():
    secrets = {
        'MAIL_PASSWORD':'YourPasswordHere',
        'MAIL_USERNAME':'YourEmailAddressHere',
        'MONGO_ADMIN': 'MongoUserNameHere',
        'MONGO_PASSWORD':'MongoPasswordHere'
        }
    return secrets