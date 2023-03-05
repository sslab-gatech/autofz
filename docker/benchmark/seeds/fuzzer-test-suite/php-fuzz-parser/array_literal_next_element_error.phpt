<?php

$i = PHP_INT_MAX;
try {
    $array = [$i => 42, new stdClass];
    var_dump($array);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

function test($x = [PHP_INT_MAX => 42, "foo"]) {}
try {
    test();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>