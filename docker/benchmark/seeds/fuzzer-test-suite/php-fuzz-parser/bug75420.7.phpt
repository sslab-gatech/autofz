<?php
class Test {
    public function __set($x,$v) { $GLOBALS["name"] = 24; var_dump($x); }
}

$obj = new Test;
$name = "foo";
$name = str_repeat($name, 2);
$obj->$name = 1;
var_dump($name);
?>