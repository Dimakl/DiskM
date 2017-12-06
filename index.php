<?php
	$db_host = 'localhost';
	$db_user = 'root';
	$db_password = 'ef37au82';
	$db_name = 'students';
	$link = mysqli_connect($db_host, $db_user, $db_password, $db_name);

	if (!$link) {
    	die('<p style="color:red">'.mysqli_connect_errno().' - '.mysqli_connect_error().'</p>');
	echo "cool";
}
	$result = mysqli_query($link, "SELECT * FROM students;");
	switch ($_GET['operation']){
		case 'all':
			echo '<p>Все пользователи: </p><ul>';
			while ($row = mysqli_fetch_row($result)) {
				$row1 = utf8_encode($row[1]);
				echo "<li>{$row[0]} {$row[1]} {$row[2]} {$row[3]} {$row[4]} {$row[5]} {$row[6]} {$row[7]}</li>";
			}
			echo '</ul>';
			break;
		case 'get':
			$contains = mysqli_query($link,"SELECT * FROM students WHERE ID={$_GET['num']};");
			if ($contains->num_rows>0){
				echo "yes";
			}
			else{
				echo "no";
			}
			break;
		case 'push':
	if(isset($_GET['name']))
	{
	$name = $_GET['name'];
	}
	if(isset($_GET['surname']))
	{
	$surname = $_GET['surname'];
	}
	if(isset($_GET['middle_name']))
	{
	$mid_name = $_GET['middle_name'];
	}
	if(isset($_GET['class_num']))
	{
	$class_num = $_GET['class_num'];
	}
	if(isset($_GET['class_let']))
	{
	$class_let = $_GET['class_let'];
	}
	if(isset($_GET['phone']))
	{
	$phone = $_GET['phone'];
	}
	if(isset($_GET['face_recog']))
	{
	$face_recog = $_GET['face_recog'];
	}

	$push = mysqli_query($link,"INSERT INTO students (`Name`,`Surname`,`Middle_name`,`Class_num`,`Class_let`,`Phone`,`face_recog`) VALUES ('$name','$surname','$mid_name','$class_num','$class_let','$phone','$face_recog')");

	if ($push==true)
	{
	echo "<br>Информация в базу добавлена успешно.";
	}
	else echo "<br>Информация в базу не добавлена.";
	}
?>