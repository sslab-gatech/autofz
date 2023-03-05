<?php

class Test {
    public int $i = 42;
    public string $s = "str";
}

$test = new Test;

$ref =& $test->i;
try {
    try {
        throw new Exception("ex");
    } catch (Exception $ref) {
        echo "Unreachable\n";
    }
} catch (TypeError $e) {
    var_dump($test->i);
    echo $e . "\n\n";
}

$ref =& $test->s;
try {
    try {
        throw new Exception("ex");
    } catch (Exception $ref) {
        echo "Unreachable\n";
    }
} catch (TypeError $e) {
    var_dump($test->s);
    echo $e . "\n\n";
}

?>