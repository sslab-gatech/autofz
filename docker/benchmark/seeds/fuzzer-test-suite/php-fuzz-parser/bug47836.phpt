<?php

$arr[PHP_INT_MAX] = 1;
try {
    $arr[] = 2;
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

var_dump($arr);
?>