<?php

class Test {
    public X $propX;
    public ?Y $propY;
}

spl_autoload_register(function($class) {
    echo "Loading $class\n";
});

$test = new Test;
try {
    $test->propX = new stdClass;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

if (true) {
    class X {}
}

$test->propX = new X;
var_dump($test->propX);

$test->propY = null;
$r =& $test->propY;
try {
    $test->propY = new stdClass;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

if (true) {
    class Y {}
}

$r = new Y;
var_dump($test->propY);

?>