<html>
	<head>
        <title>Hades fw update</title>
	</head>
	<body>
		<?php
			$uploaddir = '/home/pi/Hades_project/upload/';
			$uploadfile = $uploaddir.basename($_FILES['myfile']['name']);

			echo "<pre>";
			if (move_uploaded_file($_FILES['myfile']['tmp_name'], $uploadfile)) {
		 	   echo "Upload OK \n";
			} else {
			    echo "Upload failed \n";
			}
			print_r($_FILES);
			echo "</pre>";
		?>
	</body>
</html>
