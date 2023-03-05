<?php

try {
    test($foo = new stdClass);
    var_dump($foo);
} catch (Throwable $e) {
    echo "Exception: " . $e->getMessage() . "\n";
}
try {
    test($bar = 2);
    var_dump($bar);
} catch (Throwable $e) {
    echo "Exception: " . $e->getMessage() . "\n";
}
try {
    test($baz = &$bar);
    var_dump($baz);
} catch (Throwable $e) {
    echo "Exception: " . $e->getMessage() . "\n";
}

function test(&$param) {
        $param = 1;
}

?>