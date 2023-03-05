<?php

$arr = [1, 2, 3];
try {
    var_dump([PHP_INT_MAX-1 => 0, ...$arr]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

try {
    var_dump([PHP_INT_MAX-1 => 0, ...[1, 2, 3]]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

const ARR = [1, 2, 3];
function test($x = [PHP_INT_MAX-1 => 0, ...ARR]) {}
try {
    test();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>