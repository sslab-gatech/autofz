<?php

class Test {
    public $prop;
}

$test = new Test;
unset($test->prop);
$ref =& $test->prop;
var_dump($ref);

?>