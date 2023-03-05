<?php

class C extends _ZendTestClass {}

$obj = new _ZendTestChildClass;
$obj->classUnionProp = new stdClass;
$obj->classUnionProp = new ArrayIterator;
try {
    $obj->classUnionProp = new DateTime;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

$obj = new C;
$obj->classUnionProp = new stdClass;
$obj->classUnionProp = new ArrayIterator;
try {
    $obj->classUnionProp = new DateTime;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}

?>