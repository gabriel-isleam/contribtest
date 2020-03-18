#!/usr/bin/python3

# run as ./test.py

import subprocess
import unittest
import generate
import os

class Test(unittest.TestCase):
	# test if the function returns the path only for
	# the files with extension .rst
	def test_list_files(self):
		files_no = 0
		for file_path in generate.list_files('test/source'):
			files_no += 1
		self.assertEqual(files_no, 2)

	# test the function read_file
	def test_read_file(self):
		expected_metadata = dict()
		expected_metadata["title"] = "My awesome site";
		expected_metadata["layout"] = "home.html";
		expected_content = "blah blah";
		metadata, content = generate.read_file('test/source/index.rst')
		self.assertTrue(expected_metadata == metadata)
		self.assertTrue(expected_content == content)

	# test the creation and the content of the html file
	# in the case when the folder is already created
	def test_write_output_existing_folder(self):
		folder = 'output_test'
		file = 'test_file'
		os.makedirs(folder)
		generate.write_output(folder, file, 'just a test')
		file_path = os.path.join(folder, file + '.html')
		self.assertTrue(os.path.exists(file_path))

		result = subprocess.Popen(['cat', file_path], 
			stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = result.communicate()
		self.assertEqual(out.decode("utf-8"), 'just a test')

		os.remove(file_path)
		os.rmdir(folder)

	# test the creation of the html file and the output folder
	# in the case when the output folder is missing
	def test_write_output_missing_folder(self):
		folder = 'output_test'
		file = 'test_file'
		generate.write_output(folder, file, 'just a test')
		file_path = os.path.join(folder, file + '.html')
		self.assertTrue(os.path.exists(file_path))

		os.remove(file_path)
		os.rmdir(folder)

	# test the correctness of the html files created
	def test_all(self):
		folder_path = 'test/source'
		output_folder = 'output'
		ref_folder = 'test/expected_output'
		generate.generate_site(folder_path, output_folder)
		for file in os.listdir(output_folder):
			ref_file = os.path.join(ref_folder, file)
			result = subprocess.Popen(['diff', '-B', file, ref_file], 
				stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out, err = result.communicate()
			self.assertEqual(out.decode("utf-8"), "")
			os.remove(os.path.join(output_folder, file))

		os.rmdir(output_folder)

if __name__ == '__main__':
	unittest.main(verbosity=2)
	