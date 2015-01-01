#!/usr/bin/env python

import sys, os, datetime
import smtplib
import commands
from email.mime.text import MIMEText

from config import config

def main(argv):
	lgr = open(config["log_file"], "a")
	if len(argv) < 6:
		lgr.write("ERR: Not egnough arguments. Provided %d, expected 5. Args: %s \n" % (len(argv), str(argv)))
		sys.exit()

	action = argv[1]
	repo_path = argv[2]
	rev = int(argv[3])
	search_path = argv[4]
	email_to = argv[5]

	paths = commands.getoutput('/usr/bin/svnlook changed -r %d %s' % (rev, repo_path))
	paths_list = paths.split("\n")
	fire_notify = False
	for item in paths_list:
		path = item[4:].strip()
		if path == search_path:
			fire_notify = True
			break

	if fire_notify == False:
		sys.exit()

	email_from = config["sender"]
	email_to = argv[5]

	msg = "File '%s' was updated. Update your working copy." % search_path
	current_time = str(datetime.datetime.now())

	mail = MIMEText(msg)
	mail["Subject"] = "Repo update"
	mail["From"] = email_from
	mail["To"] = email_to

	try:
		s = smtplib.SMTP(config["smtp_url"])
		s.login(config["smtp_user"], config["smtp_pass"])
		s.sendmail(email_from, email_to, mail.as_string())
		s.quit()
		lgr.write("SENT to %s -- %s -- %s \n" % (email_to, current_time, msg))
	except:
		error = sys.exc_info()[1]
		lgr.write("smtplib ERROR -- %s -- %s \n" % (current_time, error))
		pass

	lgr.close()


if __name__ == "__main__":
	main(sys.argv)
