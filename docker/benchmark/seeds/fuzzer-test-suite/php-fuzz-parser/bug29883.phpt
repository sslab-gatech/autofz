<?php
$x = "bug";
var_dump(isset($x[-10]));
var_dump(isset($x[1]));
var_dump(isset($x["1"]));
var_dump($x[-10])."\n";
var_dump($x[1])."\n";
var_dump($x["1"])."\n";
?>