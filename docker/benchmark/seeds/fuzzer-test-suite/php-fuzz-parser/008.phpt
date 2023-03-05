<?php

try {
    var_dump(define(array(1,2,3,4,5), 1));
} catch (TypeError $e) {
    echo "TypeError: ", $e->getMessage(), "\n";
}

var_dump(define("TRUE", 1));
var_dump(define(" ", 1));
var_dump(define("[[[", 2));
var_dump(define("test const", 3));
var_dump(define("test const", 3));
var_dump(define("test", array(1)));
var_dump(define("test1", fopen(__FILE__, 'r')));
var_dump(define("test2", new stdclass));

var_dump(constant(" "));
var_dump(constant("[[["));
var_dump(constant("test const"));

echo "Done\n";
?>