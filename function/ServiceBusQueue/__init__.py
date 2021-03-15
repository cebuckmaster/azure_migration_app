import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = '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'

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    try:
        conn = psycopg2.connect("dbname='techconfdb' user='azureadmin@postgresdb-server' host='postgresdb-server.postgres.database.azure.com' password='Azureisfun1!' sslmode='true'")
        cur = conn.cursor()
        cur.execute("""SELECT message, subject FROM notification WHERE id = %s""", str(notification_id))
        notifications = cur.fetchone()
        personalized_subject = notifications[1]

        # TODO: Get attendees email and name
        cur.execute("""SELECT CONCAT(last_name, ', ', first_name) as full_name, email FROM attendee""")
        rows = cur.fetchall()

        attendee_counter = 0
        # TODO: Loop through each attendee and send an email with a personalized subject
        for row in rows:
            attendee_counter += 1
            send_email(row[1], personalized_subject)

        status_msg = 'Notified ' + str(attendee_counter)
        now = datetime.now()

        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        cur.execute("""UPDATE notification SET completed_date = %s, status = %s WHERE id = %s""", (dt_string, status_msg, str(notification_id)))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        conn.close()
        # TODO: Close connection

def send_email(email, subject):
    message = Mail(
        from_email='cebuckmaster@gmail.com',
        to_emails=email,
        subject=subject,
        plain_text_content='Notification')

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)