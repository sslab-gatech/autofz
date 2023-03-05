<?php

class Test {
    public int|string $x;
    public float|string $y;
}

$test = new Test;
$r = "foobar";
$test->x =& $r;
$test->y =& $r;

$v = 42;
try {
    $r = $v;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($r, $v);

$v = 42.0;
try {
    $r = $v;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($r, $v);

unset($r, $test->x, $test->y);

$test->x = 42;
try {
    $test->y =& $test->x;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

unset($test->x, $test->y);

$test->y = 42.0;
try {
    $test->x =& $test->y;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>