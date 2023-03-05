<?php
class Test implements ArrayAccess {
    public function offsetExists($x) { }
    public function offsetGet($x) { }
    public function offsetSet($x, $y) { $GLOBALS["obj"] = 24; var_dump($this); }
    public function offsetUnset($x) { }
}

$obj = new Test;
$name = "foo";
$obj[$name] = 1;
var_dump($obj);
?>