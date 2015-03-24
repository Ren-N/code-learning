#!/usr/bin/python
# coding: utf-8

import cgi
import os
import subprocess
import commands

GCC_CMD   = "/usr/local/bin/gcc-4.9"
CPP_CMD   = "/usr/local/bin/g++-4.9"
JAVAC_CMD = "/usr/bin/javac"
JAVA_CMD  = "/usr/bin/java"
PY_CMD    = "/usr/bin/python"
RB_CMD    = "/usr/bin/ruby"

# カレントディレクトリ変更.
# path = "/Users/ren/" #絶対パス
# os.chdir(os.path.dirname(path))

#️ subprocessでは実行できない
# p = subprocess.Popen(['/bin/ls'], stdout=subprocess.PIPE)
# print p.stdout.readline()
# print p.communicate()[0]

def compile(lang,filename):
	out = ""
	if lang == 'c':
		out = commands.getoutput( GCC_CMD + ' -o code ' + filename)
		out = commands.getoutput('./code')
	elif lang == 'cpp':
		commands.getoutput( CPP_CMD + ' -o code ' + filename)
		out = commands.getoutput('./code')
	elif lang == 'java':
		# コンパイル作業をmkdirで作ったディレクトリでやり,終わったら削除したほうがいいかもしれない.
		commands.getoutput( "rm ./*.class" )
		commands.getoutput( JAVAC_CMD + " " + filename )
		classname = commands.getoutput("/bin/ls | grep '^[A-Z].*\.class'")
		classname = classname.split('.')[0]
		out = commands.getoutput( JAVA_CMD + " " + classname)
	elif lang == 'js':
		out = '未対応'
	elif lang == 'py':
		out = commands.getoutput( PY_CMD + " " + filename )
	elif lang == 'rb':
		out = commands.getoutput( RB_CMD + " " + filename)
	return out



# POST取得時に実行.
if os.getenv('REQUEST_METHOD') == "POST":
	# POSTのデータ取得.
	form = cgi.FieldStorage()
	code = form.getvalue('code', 'none')
	lang = form.getvalue('lang', 'none')

	# ファイル作成.
	filename = 'code.' + lang
	f = open(filename, "w")
	f.write(code)
	f.close()
	
	# HTML出力
	print 'Content-Type: text/html\n\n'
	print '<html><body>\n'
	print compile(lang,filename)
	print '</body></html>'
	print ""



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








