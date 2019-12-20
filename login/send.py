import smtplib
from fundoo.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD

request_smtp = smtplib.SMTP('smtp.gmail.com', 587)
request_smtp.starttls()
request_smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
message = "Sending Message"
request_smtp.sendmail(EMAIL_HOST_USER, "srmsa786@gmail.com", message)
request_smtp.quit()