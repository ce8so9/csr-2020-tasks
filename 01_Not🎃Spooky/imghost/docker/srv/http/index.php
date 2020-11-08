<?php

function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

session_start();

if(session_id() == "pybu3zheoyeupyzgodcrxf7oqc") {
  $_SESSION["uploads"] = array(array("name"=>"flag.txt","file"=>"iKZ1cjWDNEbab688tUVB.txt"));
}
if(!array_key_exists("uploads", $_SESSION)) $_SESSION["uploads"] = array();
if(!file_exists("/dev/shm/uploads")) mkdir("/dev/shm/uploads");
if(!file_exists("/dev/shm/tmp-uploads")) mkdir("/dev/shm/tmp-uploads");

if(!file_exists("/dev/shm/uploads/iKZ1cjWDNEbab688tUVB.txt")) {
  file_put_contents("/dev/shm/uploads/iKZ1cjWDNEbab688tUVB.txt", file_get_contents("/flag.txt"));
}
if(array_key_exists("file", $_FILES)) {
  if(strpos($_POST["type"], '.') !== false) {
    die("Illegal filetype detected, police has been contacted, go to hacker jail.");
  }
  $filename = generateRandomString(20) . '.' . $_POST['type'];
  $filename = str_replace("%", "", $filename);
  move_uploaded_file($_FILES["file"]["tmp_name"], "/dev/shm/uploads/" . $filename);
  $_SESSION["uploads"][] = array("name" => $_FILES["file"]["name"], "file" => $filename);
  header("Location: /");
  die();
}

if($_SESSION["uploads"]) {
  echo '<h4>Your files</h4>';
  echo '<ul>';
  foreach($_SESSION["uploads"] as $filearr) {
    $path_parts = pathinfo($filearr["file"]);
    if($path_parts["extension"] == "txt") {
      echo '<li><a href="/uploads/' . $filearr["file"] . '">' . $filearr["name"] . '</a></li>';
    } else {
      echo '<li><a href="/i/' . $filearr["file"] . '">' . $filearr["name"] . '</a></li>';
    }
  }
  echo '</ul>';
}

echo '
<h4>Upload new file</h4>
<form action="?upload" method="post" enctype="multipart/form-data">
<input type="file" name="file" /></td>
<select name="type">
<option>png</option>
<option>jpg</option>
<option>txt</option>
</select>
<input type="submit" value="Upload" />
</form>
';

?>
