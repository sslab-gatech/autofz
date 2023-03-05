<?php

class Test {
    public int $foo;
}

$test = new Test;

$test->foo = PHP_INT_MIN;
try {
    --$test->foo;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);
try {
    $test->foo--;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);

$test->foo = PHP_INT_MAX;
try {
    ++$test->foo;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);
try {
    $test->foo++;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);

// Do the same things again, but with the property being a reference.
$ref =& $test->foo;

$test->foo = PHP_INT_MIN;
try {
    --$test->foo;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);
try {
    $test->foo--;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);

$test->foo = PHP_INT_MAX;
try {
    ++$test->foo;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);
try {
    $test->foo++;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($test->foo);

?>