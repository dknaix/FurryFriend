function check_cookie_preset(){//ajax chk
	// alert("Parentcookie_prechk_called")
	$.post("validate.php",{check:"123"},
	function(data, status){
		if (data=="already_set"){
			// alert("prechk Set!!! data:"+data)
			$("#logout_btn_main").fadeIn(50)
			}
		else{
			// alert("prechk not_set data:"+data)
			$("#logout_btn_main").fadeOut(50)
			}
		}
	);
}


function logout(){
	$.post("validate.php",{logout:123},
	function(data, status){
		alert("Data:"+data+" Status:"+status)

		if (data=="logout_success"){
			$("#logout_btn_main").fadeOut(50)
			$("#iframe0").attr("src","ff_home.html").delay(100)
		}
		else {alert("Err in logout")}
	});
}
