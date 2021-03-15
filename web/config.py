import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="postgresdb-server.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="azureadmin@postgresdb-server" #TODO: Update value
    POSTGRES_PW="Azureisfun1!"   #TODO: Update value
    POSTGRES_DB="techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
#    SECRET_KEY = '4VBLzdn2cOdQkWJfciJl3z25h9be3kXs5Dm3Xre3kKQ='
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://app-migration-cebuck.servicebus.windows.net/;SharedAccessKeyName=sendnotification;SharedAccessKey=qbEkjHuY3aNd0q2EDmsppPPPngf11SlznHGy6ZbiE8o=;EntityPath=servicebusqueue' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='servicebusqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False