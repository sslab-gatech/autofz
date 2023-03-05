<?php

function f(...$args) {
    var_dump(count($args));
}

$array = array_fill(0, 10000, 42);
f(...$array, ...$array);

?>