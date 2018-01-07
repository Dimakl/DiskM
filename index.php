<?php
	$db_host = 'localhost';
	$db_user = 'usr';
	$db_password = 'pass';
	$db_name = 'students';
	$link = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8", $db_user, $db_password, array(
		PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
		PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
	));
	if (!$link) {
    	die('<p style="color:red">'.mysqli_connect_errno().' - '.mysqli_connect_error().'</p>');
	}
	$result = array();
	switch ($_GET['operation']){
		case 'all': {
			$result = $link->query("SELECT * FROM students;")->fetchAll();
			break;
		}
		case 'id': {
			$statement = $link->prepare("SELECT * FROM students WHERE ID = :ID");
			$result = $statement->execute(array(':ID' => $_GET['id']));
			break;
		}
		case 'push': {
			$fields = array ('name', 'surname', 'middle_name', 'class_num', 'class_let', 'phone', 'face_recog');
			foreach($fields as $field){
				$to_ins[':' . $field] = isset($_POST[$field]) ? trim($_POST[$field]) : '';
			}
			unset($value);
			$statement = $link->prepare("
				INSERT INTO students (`Name`,`Surname`,`Middle_name`,`Class_num`,`Class_let`,`Phone`,`face_recog`) 
				VALUES (:name, :surname, :middle_name, :class_num, :class_let, :phone, :face_recog)");
			$statement->execute($to_ins);
			$result['id'] = $link->lastInsertId();
			break;
		}
	}
	echo json_encode($result);
?>
