<?php

spl_autoload_register(function($classname) {
    if (in_array($classname, array('a','b','c'))) {
        require_once __DIR__ . "/{$classname}.inc";
    }
});

set_error_handler(function ($errno, $errstr, $errfile, $errline) {
    var_dump($errstr);
}, error_reporting());

a::staticTest();

$b = new b();
$b->test();