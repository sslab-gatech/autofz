<?php

$str = "Sitting on a corner all alone, staring from the bottom of his soul";

var_dump($str[1]);
var_dump($str[0.0836]);
var_dump($str[NULL]);
var_dump($str["run away"]);
var_dump($str["13"]);
var_dump($str["14.5"]);
var_dump($str["15 and then some"]);

var_dump($str[TRUE]);
var_dump($str[FALSE]);

$fp = fopen(__FILE__, "r");
try {
    var_dump($str[$fp]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

$obj = new stdClass;
try {
    var_dump($str[$obj]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

$arr = Array(1,2,3);
try {
    var_dump($str[$arr]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

echo "Done\n";
?>