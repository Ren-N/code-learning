


function init(){
	window.scrollTo(0,0);
	$(window).scroll(function () {
		var s = $(this).scrollTop();
		$('#backboard').css('background-position', '0 ' + parseInt( -s / 20 ) + 'px');
  });

}