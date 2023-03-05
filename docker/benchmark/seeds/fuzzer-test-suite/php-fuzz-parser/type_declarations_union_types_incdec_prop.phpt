<?php

class Test {
    public int|float $prop;
    public int|bool $prop2;
}

/* Incrementing a int|float property past int min/max is legal */

$test = new Test;
$test->prop = PHP_INT_MAX;
$x = $test->prop++;
var_dump(is_double($test->prop));

$test->prop = PHP_INT_MAX;
$x = ++$test->prop;
var_dump(is_double($test->prop));

$test->prop = PHP_INT_MIN;
$x = $test->prop--;
var_dump(is_double($test->prop));

$test->prop = PHP_INT_MIN;
$x = --$test->prop;
var_dump(is_double($test->prop));

$test = new Test;
$test->prop = PHP_INT_MAX;
$r =& $test->prop;
$x = $test->prop++;
var_dump(is_double($test->prop));

$test->prop = PHP_INT_MAX;
$x = ++$test->prop;
$r =& $test->prop;
var_dump(is_double($test->prop));

$test->prop = PHP_INT_MIN;
$x = $test->prop--;
$r =& $test->prop;
var_dump(is_double($test->prop));

$test->prop = PHP_INT_MIN;
$x = --$test->prop;
$r =& $test->prop;
var_dump(is_double($test->prop));

/* Incrementing a non-int|float property past int min/max is an error,
 * even if the result of the overflow (a float) would technically be allowed
 * under a type coercion. */

try {
    $test->prop2 = PHP_INT_MAX;
    $x = $test->prop2++;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MAX;
    $x = ++$test->prop2;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MIN;
    $x = $test->prop2--;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MIN;
    $x = --$test->prop2;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MAX;
    $r =& $test->prop2;
    $x = $test->prop2++;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MAX;
    $r =& $test->prop2;
    $x = ++$test->prop2;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MIN;
    $r =& $test->prop2;
    $x = $test->prop2--;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

try {
    $test->prop2 = PHP_INT_MIN;
    $r =& $test->prop2;
    $x = --$test->prop2;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>