<?php

$arr[1][2][3][4][5];

echo $arr[1][2][3][4][5];

$arr[1][2][3][4][5]->foo;

try {
    $arr[1][2][3][4][5]->foo = 1;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

$arr[][] = 2;

try {
    $arr[][]->bar = 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>