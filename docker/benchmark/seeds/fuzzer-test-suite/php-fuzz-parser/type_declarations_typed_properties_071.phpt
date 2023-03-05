<?php

class Test {
    public string $x = "x";
}

$test = new Test;
var_dump($test);
$y = "y";
$test->x = &$y;
var_dump($y, $test);

$z = 42;
$y = $z;
var_dump($y, $z, $test);

?>