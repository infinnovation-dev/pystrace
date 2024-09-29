import unittest
import os
from tempfile import NamedTemporaryFile
from strace import StraceParser

class TestCsv(unittest.TestCase):
	def test_parse_pid(self):
		# Command: strace -tttf sh -c uname -s
		# Then removed "+++ exited"... and "--- SIGCHLD"... lines
		with open(resource_path('sh-c-uname-s.trace')) as f:
			parser = StraceParser(f)
			it = parser.parse()

			entry = next(it)
			self.assertEqual(entry.syscall_name, 'execve')
			self.assertEqual(entry.syscall_arguments[1], '["sh", "-c", "uname", "-s"]')
			self.assertTrue(parser.have_pids)

			rest = list(it)
			self.assertEqual(len(rest), 111)
			self.assertEqual(rest[-1].syscall_name, 'exit_group')

	def test_parse_data(self):
		# Command: strace -ttt -e wrte=1 date
		with open(resource_path('date-w1.trace')) as f:
			entries = list(StraceParser(f).parse())
		writes = [e for e in entries if e.syscall_name == 'write']
		self.assertEqual(writes[0].data, b'Sun 29 Sep 13:06:28 BST 2024\n')

def resource_path(filename):
    """Locate a resource relative to the tests directory"""
    return os.path.join(os.path.dirname(__file__), filename)

if __name__=='__main__':
    unittest.main()
