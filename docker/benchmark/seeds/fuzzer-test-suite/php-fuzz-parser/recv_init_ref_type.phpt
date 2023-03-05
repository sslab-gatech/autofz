<?php

function test(array &$foo = []) {
}

try {
    $bar = 42;
    test($bar);
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>