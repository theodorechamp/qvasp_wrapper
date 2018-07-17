import paramiko
import time


class SSHClient:
	def __init__(self, u, p, h, po):
		self.hostname = h
		self.username = u
		self.password = p
		self.port = po
		self.client = paramiko.SSHClient()
		self.lastcheckqueue = 0.0

	def connect(self):
		self.client.load_system_host_keys()
		print("Waiting for Duo response...")
		self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
		self.cwd = "./"
		self.sftp = self.client.open_sftp()

	def command(self, cmd, echo=False):
		fullcmd = "cd " + self.cwd + "; " + cmd
		stdin, stdout, stderr = self.client.exec_command(fullcmd)
		time.sleep(.05)
		if echo:
			print(stdout.read())
		return stdout.read()

	def cd(self, newdir, relative=False):
		if relative:
			self.cwd = self.cwd + newdir
		else:
			self.cwd = newdir

	def changeFTPdir(self, newdir, relative=False):
		if not relative:
			self.sftp.chdir()
		self.sftp.chdir(newdir)

	def downloadFTP(self, server, local):
		self.sftp.get(server, local)

	def uploadFTP(self, server, local , echoserver=False, echoclient=False):
		if echoserver:
			print(server)
		if echoclient:
			print(local)
		self.sftp.put(local, server)


	def inqueue(self, mat):
		if (time.time() - self.lastcheckqueue) > 600:
			self.updatequeue()
		mybool = False
		logfile = mat.generatelog()
		for x in self.queue:
			if x.find(logfile[:7]) != -1:
				mybool = True
		return mybool

	def updatequeue(self):
		strqueue = self.command("squeue")
		self.queue = strqueue.splitlines()
		for x in list(self.queue):
			if x.find("thch0696") == -1:
				self.queue.remove(x)
		print("Updated queue")
		self.lastcheckqueue = time.time()

	def showcwd(self):
		print(self.cwd)