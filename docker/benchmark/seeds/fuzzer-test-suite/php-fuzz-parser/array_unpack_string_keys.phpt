<?php
$y = [1, 2, 3];
$z = "bar";
$x = [...$y, "foo" => $z];
var_dump($x);
?>