<?php

class Test {
    public static int $x = 0;
}

class Test2 extends Test {
    public static $y = 1;
}

$x =& Test::$x;
try {
    $x = "foo";
} catch (TypeError $e) { echo $e->getMessage(), "\n"; }
var_dump($x, Test::$x);

Test::$x =& Test2::$y; // remove the typed ref from $x
$x = "foo";
var_dump($x, Test::$x);

?>