(function($){
	
	$(document).ready(function(){
	
		$("select").each(function(){
			$(this).wrap("<div class='s_wrap_1'></div>")
				.wrap("<div class='s_wrap_2'></div>");
			$(this).parent().after("<div class='s_btn_1'></div>");
		});	
		$(".s_btn_1").click(function(){
				$(this).prev(".s_wrap_2").find("select").select();
				return false;
		});
	});

 })(jQuery);
