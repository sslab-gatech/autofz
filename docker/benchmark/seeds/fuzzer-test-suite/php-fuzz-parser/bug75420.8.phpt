<?php
class Test {
    public function __set($x,$v) { $GLOBALS["obj"] = 24; var_dump($this); }
}

$obj = new Test;
$name = "foo";
$obj->$name = 1;
var_dump($obj);
?>