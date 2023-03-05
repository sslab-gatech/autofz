<?php
class Overloaded {
    function __set($r, $a) {}
}
$obj = new Overloaded;
$x = $obj->prop = new stdClass;
var_dump($x);
?>