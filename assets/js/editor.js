
var editor;
function init(){
	// editor initialize -------------
    // document.getElementById( 'editor' ).innerHTML = document.getElementById( 'text' ).value;
    // or editor.setValue( "the new text here" ); 
    // innerHTMLだと #include <...> の <...>がタグと認識されエディタから消えてしまう.
    editor = ace.edit( 'editor' );
    editor.setTheme( 'ace/theme/monokai' );
    // editor.getSession().setMode( 'ace/mode/c_cpp' );
    document.getElementById( 'editor' ).style.fontSize = '14';
    editor.getSession().on('change', function(){
    	// 更新時に現在の文字をtextariaに避難.
        var textcode = editor.getSession().getValue();
        document.getElementById( 'text' ).value = textcode;
    });
    // --------------------------------
    // editorの言語設定.
    var selecter = document.getElementById('selectedLang');
	var lang = selecter.options[selecter.selectedIndex].value;
    setEditorMode(lang);
	setTabName('code.'+lang);
	// keybind emacs
	editor.setKeyboardHandler("ace/keyboard/emacs");
	editor.commands.addCommand({
		Name : "savefile",
		bindKey: {
			win : "Ctrl-Shift-S",
			mac : "Ctrl-Shift-S"
		},
		exec: function(editor) {
			onSaveFile();
		}
	});
	// エディタに文字がなければ, 注意書きを書く.
	text = document.getElementById( 'text' ).value;
	if(text !== ""){
		editor.getSession().setValue(text);
	}else{
		var warn = Array(2);
		warn[0] = "[注意]";
		warn[1] = "Javaのクラス名はCodeにしてください.";
		var cmtout;
		switch(lang){
			case 'c':
			case 'cpp':
			case 'java':
			case 'js':
					cmtout = "// "
				break;
			case 'py':
			case 'rb':
					cmtout = "# "
				break;
			default:
					cmtout = "// "
				break;
		}
		var comment = "";
		for(var i=0; i<warn.length; i++){
			comment = comment + cmtout+warn[i]+"\n";
		}
		// editor.getSession().setValue(comment);
	}
	
}

function setEditorMode(lang){
	var mode = getLangInfo(lang)[1];
	if(editor !== null){
	    editor.getSession().setMode( mode );
	}else{
		console.log("editor not define. check init().");
	}
}
function onSaveFile(){

}

C_TMPL ="#include <stdio.h>\n\nint main(void){\n\tprintf(\"Hello World\\n\");\n\treturn 0;\n}"
CPP_TMPL ="#include <iostream>\n\nint main( ){\n\tstd::cout << \"Hello World!\\n\";\n}"
JAVA_TMPL="class Template {\n\tpublic static void main(String[ ] args){\n\t\tSystem.out.println(\"Hello World\");\n\t}\n}"
JS_TMPL="console.log(\"Hello World\");"
PY_TMPL="# -*- coding: utf-8 -*-\n\nif __name__ == \"__main__\":\n\tprint \"Hello World\""
RB_TMPL="if __FILE__ == $0 then\n\tprint(\"Hello World\\n\")\nend"

function getLangInfo(lang){
	var info = Array(3);
	switch(lang){
		case 'c':
			info[0] = C_TMPL;
			info[1] = 'ace/mode/c_cpp';
			info[2] = 'gcc'
			break;
		case 'cpp':
			info[0] = CPP_TMPL;
			info[1] = 'ace/mode/c_cpp';
			info[2] = 'g++'
			break;
		case 'java':
			info[0] = JAVA_TMPL;
			info[1] = 'ace/mode/java';
			info[2] = 'javac'
			break;
		case 'js':
			info[0] = JS_TMPL;
			info[1] = 'ace/mode/javascript';
			info[2] = 'none'
			break;
		case 'py':
			info[0] = PY_TMPL;
			info[1] = 'ace/mode/python';
			info[2] = 'python'
			break;
		case 'rb':
			info[0] = RB_TMPL;
			info[1] = 'ace/mode/ruby';
			info[2] = 'ruby'
			break;
	}
	return info;
}
// 「テンプレート」ボタンを押したとき実行
function setTemplate(){
	swal({
		title: "Are you sure?",
	    text: "現在のコードは削除されますがいいですか？",
	    type: "warning",
	    showCancelButton: true,
	    confirmButtonColor: "#DD6B55",
	    confirmButtonText: "Paste!",
	    closeOnConfirm: false
	},
	function(){
		swal("Paste Code!","","success");
		//テンプレートを貼り付ける.
		var selecter = document.getElementById('selectedLang');
		var lang = selecter.options[selecter.selectedIndex].value;
		var info = getLangInfo(lang);
		var template = info[0];
		var mode = info[1]
		editor.setValue( template );
    	editor.getSession().setMode( mode );
	    //貼り付けしたあと、全選択になっているので、カーソルを行末にする.
    	editor.navigateLineEnd();
	});
}
// 「コンパイル」ボタンを押したとき実行
function compile(){
	startCompileAnimation();
	var selecter = document.getElementById('selectedLang');
	var lang = selecter.options[selecter.selectedIndex].value;
	var data = { 
		lang : lang,
		code : editor.getValue() 
	};
	var url = "CGI/compile.py";
	multiPost(url,data);
	
}

function multiPost(url,data){
	//サーバーに送信.
	var request =  new XMLHttpRequest();
	request.open("POST", url, true);
	//form-data,POST送信
	boundary = "-----";
    request.setRequestHeader("content-type",
                         "multipart/form-data; boundary="+boundary);
    var senddata = "";
    for (name in data) {
      senddata += "--"+boundary+"\r\n"+
        "Content-Disposition: form-data; name=\""+name+"\"\r\n\r\n"+
        data[name]+"\r\n";
    }
    senddata += "--"+boundary+"--\r\n";
	//ハンドラ.
	request.onreadystatechange = function() {
		if (request.readyState == 4 && request.status == 200) {
			//受信完了時の処理.
			var exec = "run code."+data['lang'];
			var header = "$ " + exec + "<br><br>"
			var terminal = document.getElementById('csl-box');
			terminal.innerHTML = header + decodeURI(request.responseText).replace(/\r?\n/g, '<br>');
			stopCompileAnimation();
		}
	}
    request.send(senddata);  
}

function post(url,data){
	//サーバーに送信.
	var request =  new XMLHttpRequest();
	request.open("POST", url, true);
	//form-data,POST送信
    request.setRequestHeader("content-type","application/x-www-form-urlencoded;charset=UTF-8");
    var senddata = "";
    for (name in data) {
      if (senddata != "")
        senddata += "&";
      senddata += name+"="+escape(data[name]);
    }
    request.send(senddata); 
	//ハンドラ.
	request.onreadystatechange = function() {
		if (request.readyState == 4 && request.status == 200) {
			//受信完了時の処理.
			var exec = "run code."+data['lang'];
			var header = "$ " + exec + "<br><br>"
			var terminal = document.getElementById('csl-box');
			terminal.innerHTML = header + decodeURI(request.responseText).replace(/\r?\n/g, '<br>');
			stopCompileAnimation();
		}
	}
    request.send(senddata);  
}


function startCompileAnimation(){
	document.getElementById('loader').style.display = 'block';
}

function stopCompileAnimation(){
	document.getElementById('loader').style.display = 'none';
}
//言語選択のselecterが変更されたとき実行
function changeLang(){
	var selecter = document.getElementById('selectedLang');
	var lang = selecter.options[selecter.selectedIndex].value;
	setTabName('code.'+lang);
	setEditorMode(lang);
}

// Tabのファイル名変更
function setTabName (name) {
	document.getElementById('tab-filename').innerHTML = name;
}


