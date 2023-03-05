<?php

// Internal typed properties

$obj = new _ZendTestClass;
var_dump($obj->intProp);
try {
    $obj->intProp = "foobar";
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
$obj->intProp = 456;

try {
    $obj->classProp = $obj;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
$obj->classProp = new stdClass;
var_dump($obj);

// Inherit from internal class

class Test extends _ZendTestClass {
}

$obj = new Test;
var_dump($obj->intProp);
try {
    $obj->intProp = "foobar";
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
$obj->intProp = 456;

try {
    $obj->classProp = $obj;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
$obj->classProp = new stdClass;
var_dump($obj);

// Static internal typed properties

var_dump(_ZendTestClass::$staticIntProp);
try {
    _ZendTestClass::$staticIntProp = "foobar";
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
_ZendTestClass::$staticIntProp = 456;
var_dump(_ZendTestClass::$staticIntProp);

?>