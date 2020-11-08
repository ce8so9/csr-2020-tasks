<?php

if(!file_exists("/dev/shm/reports")) die();

$files = scandir("/dev/shm/reports");
foreach($files as $file) {
	if($file != "." && $file != ".." && $file != "") {
		echo filemtime("/dev/shm/reports/" . $file) . ";" . $file . "\n";
		if($_GET["delete"] == $file) unlink("/dev/shm/reports/" . $file);
	}
}

?>
