import unittest
import os
from tempfile import NamedTemporaryFile
from strace2csv import convert2csv

class TestCsv(unittest.TestCase):
	def test_csv_pid(self):
		# Command: strace -tttf sh -c uname -s
		# Then removed "+++ exited"... and "--- SIGCHLD"... lines
		with NamedTemporaryFile('w+') as tmp:
			convert2csv(resource_path('sh-c-uname-s.trace'),
						tmp.name)
			tmp.seek(0)
			output = list(tmp.readlines())
		self.assertEqual(len(output), 113)
		self.assertEqual('PID,TIMESTAMP,SYSCALL,CATEGORY,SPLIT,ARGC,ARG1,ARG2,ARG3,ARG4,ARG5,ARG6,RESULT,ELAPSED\n',
						 output[0])
		self.assertEqual('164843,1727596765.636300,"execve",,0,3,"""/usr/bin/sh""","[""sh"", ""-c"", ""uname"", ""-s""]","0x7ffe827fc560 /* 49 vars */",,,,0,\n',
						 output[1])
		self.assertEqual('164844,1727596765.642294,"write","IO",0,3,"1","""Linux\\n""","6",,,,6,\n',
						 output[105])

def resource_path(filename):
    """Locate a resource relative to the tests directory"""
    return os.path.join(os.path.dirname(__file__), filename)

if __name__=='__main__':
    unittest.main()
