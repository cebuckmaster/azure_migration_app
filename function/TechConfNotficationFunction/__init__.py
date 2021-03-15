import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


SENDGRID_API_KEY = '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'

def main(req: func.HttpRequest) -> func.HttpResponse:

    notification_id = req.params.get('id')
    print("id from api -> " + notification_id)


    if notification_id:
        try:
            conn = psycopg2.connect("dbname='techconfdb' user='azureadmin@postgresdb-server' host='postgresdb-server.postgres.database.azure.com' password='Azureisfun1!'")
            cur = conn.cursor()
            cur.execute("""SELECT message, subject FROM notification WHERE id = %s""", notification_id )
            row_count = cur.rowcount

            print("row count-> " + str(row_count))
            notifications = cur.fetchone()

            print(notifications)

            personalized_subject = notifications[1]

#         # TODO: Get attendees email and name
            cur.execute("""SELECT CONCAT(last_name, ', ', first_name) as full_name, email FROM attendee""")
            rows = cur.fetchall()

            attendee_counter = 0

#         # TODO: Loop through each attendee and send an email with a personalized subject
            for row in rows:
                attendee_counter += 1
                print(row)
                send_email(row[1], personalized_subject)


            status_msg = 'Notified ' + str(attendee_counter)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
            print(dt_string)

            cur.execute("""UPDATE notification SET completed_date = %s, status = %s WHERE id = %s""", (dt_string, status_msg, notification_id))
            updated_rows = cur.rowcount
            print(updated_rows)
            conn.commit()
            cur.close()
            return func.HttpResponse(str(updated_rows))

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
        finally:
            conn.close()

def send_email(email, subject):
    message = Mail(
                from_email='cebuckmaster@gmail.com',
                to_emails=email,
                subject=subject,
                plain_text_content='Notification')

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
