<?php
class Test {
    public function __isset($x) { $GLOBALS["name"] = 24; return true; }
    public function __get($x) { var_dump($x); return 42; }
}

$obj = new Test;
$name = "foo";
$name = str_repeat($name, 2);
var_dump($obj->$name ?? 12);
var_dump($name);
?>