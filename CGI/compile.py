#!/usr/bin/python
# coding: utf-8

import cgi
import os
import subprocess
import codecs
# import traceback


# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# subprocess.call(["redis-server","/home/shell/redis.conf"])

# カレントディレクトリ変更.
# path = "/Users/ren/" #絶対パス
# os.chdir(os.path.dirname(path))

# p = subprocess.Popen(['/bin/ls'], stdout=subprocess.PIPE)
# print p.stdout.readline()
# print p.communicate()[0]

if os.getenv('REQUEST_METHOD') == "POST" :
	# POSTのデータ取得.
	form = cgi.FieldStorage()
	code = form.getvalue('code', 'none')
	lang = form.getvalue('lang', 'none')

	# ファイル作成.
	# filename = 'code.' + lang
	# f = open(filename, "w")
	# f.write(code)
	# f.close()
	# file(os.path.join('/tmp', item.filename), 'wb')

	# プログラム実行.
	# out = ""
	# if lang == 'c':
	# 	tmp = subprocess.Popen(['/bin/gcc','-o','code',filename], stdout=subprocess.PIPE)
	# 	out = subprocess.Popen(['./code'],stdout=subprocess.PIPE)
	# elif lang == 'cpp':
	# 	tmp = subprocess.Popen(['/bin/gcc','-o','code',filename], stdout=subprocess.PIPE)
	# 	out = subprocess.Popen(['./code'],stdout=subprocess.PIPE)
	# elif lang == 'java':
	# 	# コンパイル作業をmkdirで作ったディレクトリでやり,終わったら削除したほうがいいかもしれない.
	# 	tmp = subprocess.Popen("rm ./*.class",shell=True, stdout=subprocess.PIPE)
	# 	tmp = subprocess.Popen(['javac',filename], stdout=subprocess.PIPE)
	# 	classname = subprocess.Popen("/bin/ls | grep *.class",shell=True, stdout=subprocess.PIPE)
	# 	out = subprocess.Popen(['java',classname])
	# elif lang == 'js':
	# 	out = '未対応'
	# elif lang == 'py':
	# 	out = subprocess.Popen(['/bin/python','code.py'],stdout=subprocess.PIPE)
	# elif lang == 'rb':
	# 	out = subprocess.Popen(['/bin/ruby','code.rb'],stdout=subprocess.PIPE)

	# HTML
	print 'Content-Type: text/html\n\n'
	print '<html><body>\n'
	print "aaaaaa"
	# print os.path.abspath(__file__)  # スクリプトの絶対パス
	print '</body></html>'

# TEST
if False :
	
	# code = "#include <stdio.h> \nint main(void){printf(\"Hello World\\n\");return 0;}"
	# code = "#include <iostream>\nint main( ){	std::cout << \"Hello World!\\n\";}"
	# code = "#!/usr/bin/python\n# -*- coding: utf-8 -*-\n\nif __name__ == \"__main__\":\n\tprint \"Hello World\"\n"
	# code = "if __FILE__ == $0 then\n\tprint(\"Hello World\\n\")\nend"
	lang = 'rb'

	# ファイル作成.
	filename = 'code.' + lang
	f = open(filename, "w")
	f.write(code)

	# プログラム実行.
	out = ""
	if lang == 'c':
		tmp = subprocess.Popen(['gcc-4.9','-o','code',filename], stdout=subprocess.PIPE)
		out = subprocess.Popen(['./code'],stdout=subprocess.PIPE)
	elif lang == 'cpp':
		tmp = subprocess.Popen(['g++-4.9','-o','code',filename], stdout=subprocess.PIPE)
		out = subprocess.Popen(['./code'],stdout=subprocess.PIPE)
	elif lang == 'java':
		# コンパイル作業をmkdirで作ったディレクトリでやり,終わったら削除したほうがいいかもしれない.
		tmp = subprocess.Popen("rm ./*.class",shell=True, stdout=subprocess.PIPE)
		tmp = subprocess.Popen(['javac',filename], stdout=subprocess.PIPE)
		classname = subprocess.Popen("/bin/ls | grep *.class",shell=True, stdout=subprocess.PIPE)
		out = subprocess.Popen(['java',classname])
	elif lang == 'js':
		out = '未対応'
	elif lang == 'py':
		out = subprocess.Popen(['python','./code.py'],stdout=subprocess.PIPE)
		out = '未対応'
	elif lang == 'rb':
		out = subprocess.Popen(['ruby','code.rb'],stdout=subprocess.PIPE)
		out = '未対応'

	# HTML
	print 'Content-Type: text/html\n\n'
	print '<html><body>\n'
	print out.communicate()[0]
	print '</body></html>'



#####################################
# 実行ユーザー
# import os
# import pwd
# print os.getuid()						->	70
# print pwd.getpwuid(os.getuid())[0]	->	_www
# print os.getlogin()					->	_securityagent
# print os.environ.get('LOGNAME')		->	None
# print os.environ.get('USER')			-> None

# スクリプトの絶対パス
# print os.path.abspath(__file__)		->  /Users/ren/Dev/Sites/code-learning/CGI








