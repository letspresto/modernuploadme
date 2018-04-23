import os 
import subprocess
import jsonify


def run_bazel():

	# cmd = ['im2txt/bazel-bin/im2txt/run_inference --checkpoint_path="im2txt/model.ckpt-3000000" --vocab_file="im2txt/word_counts.txt" --input_files="uploads/'+ photofile + '"']
	cmd = ['im2txt/bazel-bin/im2txt/run_inference --checkpoint_path="im2txt/model.ckpt-3000000" --vocab_file="im2txt/word_counts.txt" --input_files="uploads/festival.jpg"']

	# try:
	#     p = subprocess.check_output(cmd, shell=True).stdout
	# except subprocess.CalledProcessError as exc:
	#     result = exc.output

	p = subprocess.check_output(cmd, shell=True)
    # get the result
	result = str(p,'utf-8')
	result = result.split("0)")[1].split("(")[0].strip().split(".")[0].strip()

	print (result)

run_bazel()

