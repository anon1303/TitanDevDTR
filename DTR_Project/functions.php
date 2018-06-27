<?php
	include("conect.php");
	session_start();


	function submitLogin($username,$password){
		GLOBAL $connect;

		$sql = "SELECT username FROM admin WHERE username = '$username'";
		$query = mysqli_query($connect, $sql);
		$result = mysqli_fetch_array($query);

		if($result['username'] == $username) {
			$_SESSION['username'] = $result['username'];

				echo "<script> alert('Login Successfully'); window.location='home.php'; </script>";
		} else {
			echo "<script> alert('Failed to Login'); window.location='index.php'; </script>";
		}

	}