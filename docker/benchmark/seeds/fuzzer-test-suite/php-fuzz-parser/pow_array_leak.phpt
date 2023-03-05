<?php

$x = [0];
try {
    $x **= 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($x);

$x = [0];
try {
    $x **= $x;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
var_dump($x);

?>