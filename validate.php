<?php

	session_start();

	if($_SERVER["REQUEST_METHOD"] == "POST"){

		$host = "192.168.0.106";
		$port = 9999;

		if (isset($_POST["check"])) { //check cookie
			if(isset($_COOKIE['FurryFriend_Access'])) {echo "already_set";}
			else {echo "not_set";}
			exit();
		}

		//Chk login from DB
		if (isset($_POST["login"]) && isset($_POST["pass"]) && $_POST["type"]=="login" ) {
			$login_chk=$_POST["login"];
			$pass_chk=$_POST["pass"];
			$pass_chk=md5($pass_chk);

			// $host = "192.168.0.106";
			// $port = 9999;
			// No Timeout
			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=	$login_chk."--".$pass_chk."--login";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			if ($result=="login_success"){
				$cookie_name = "FurryFriend_Access";
				$cookie_value = $login_chk;
				$_SESSION["uid"] =$login_chk ; //superglobal for cookie del purpose
				// setcookie($cookie_name, $cookie_value, 0, "/");
				setcookie($cookie_name, $cookie_value, time() + (86400), "/");
			}
			else {}
			exit();
		}//end block

		//Create new acc
		if (isset($_POST["login"]) && isset($_POST["pass"]) && $_POST["type"]=="new" ) {
			$create_login=$_POST["login"];
			$create_pass=$_POST["pass"];
			$create_pass=md5($create_pass);
			// $host = "192.168.0.106";
			// $port = 9999;
			// No Timeout
			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=	$create_login."--".$create_pass."--new_acc"; //using ""--"" as seperator may cause errors if found in parameter
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);


			if ($result=="new_acc_success"){
				$cookie_name = "FurryFriend_Access";
				$cookie_value = $create_login;
				$_SESSION["uid"] =$create_login ; //superglobal for cookie del purpose
				// setcookie($cookie_name, $cookie_value, 0, "/");
				setcookie($cookie_name, $cookie_value, time() + (86400), "/");
				//write cookie after new acc created to gain access

			}

			exit();

		}//end block

		//logout block
		if ( isset($_POST["logout"]) ) {
			setcookie("FurryFriend_Access",$_SESSION["uid"], time() - (87500), "/");
			session_unset();
			echo "logout_success";
			exit();
		}

		if ( isset($_POST["p_name"]) ) {

			if ($_POST["p_cat"]=="Dog") {$target_dir = "img/items/dogs/";}
			elseif ($_POST["p_cat"]=="Cat") {$target_dir = "img/items/cats/";}
			elseif ($_POST["p_cat"]=="Fish") {$target_dir = "img/items/fish/";}
			elseif ($_POST["p_cat"]=="Bird") {$target_dir = "img/items/birds/";}
			elseif ($_POST["p_cat"]=="Extras") {$target_dir = "img/items/extras/";}


			$target_file = $target_dir . basename($_FILES["p_img"]["name"]);
			move_uploaded_file($_FILES["p_img"]["tmp_name"], $target_file);


			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=	$_POST["p_name"]."--".$_POST["p_cat"]."--".$_POST["p_cost"]."--".$_POST["p_desc"]."--".$target_file."--new_item";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}

		if ( isset($_POST["get_admin_item_list"]) ) {

			if ($_POST["get_admin_item_list"]=="order") {$message="--get_admin_order_list";}
			else {$message="--get_admin_item_list";}

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");

			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}

		if ( isset($_POST["delete_admin_item"]) ) {

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=$_POST["delete_admin_item"]."--delete_admin_item";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}


		if ( isset($_POST["contact_us_1"]) ) {

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=$_POST["contact_us_1"]."--".$_POST["contact_us_2"]."--".$_POST["contact_us_3"]."--contact_us_add";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}

		if ( isset($_POST["volunteer_ip_1"]) ) {

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=$_POST["volunteer_ip_1"]."--".$_POST["volunteer_ip_2"]."--".$_POST["volunteer_ip_3"]."--volunteer_add";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}


		if ( isset($_POST["get_admin_contact_list"]) || isset($_POST["get_admin_volunteer_list"]) ) {

			if (isset($_POST["get_admin_contact_list"])) {$message="--get_contact";}
			elseif (isset($_POST["get_admin_volunteer_list"])) {$message="--get_volunteer";}
			else {}

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			// $message=$_POST["volunteer_ip_1"]."--".$_POST["volunteer_ip_2"]."--".$_POST["volunteer_ip_3"]."--volunteer_add";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}


		if ( isset($_POST["get_client_item_list"]) ) {

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=$_POST["get_client_item_list"]."--get_client_item_list";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}

		if ( isset($_POST["get_client_item_list_cart"]) ) {

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=$_POST["get_client_item_list_cart"]."--0get_client_item_list_cart";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}

		if ( isset($_POST["post_order"]) ) {

			$acc_name=$_COOKIE['FurryFriend_Access'];

			set_time_limit(0);
			$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$con_result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
			$message=$acc_name."--".$_POST["post_order"]."--".$_POST["address"]."--".$_POST["total"]."--post_order";
			socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
			$result = socket_read ($socket, 1024) or die("Could not read server response\n");
			echo $result;
			socket_close($socket);

			exit();
		}



	}









?>
