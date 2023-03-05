<?php
class Test {
    public ?Type $prop;
}
$obj = new Test;
$ref =& $obj->prop;
try {
    $ref = [1];
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
try {
    $ary = [1];
    $ref = $ary;
} catch (TypeError $e) {
    echo $e->getMessage(), "\n";
}
var_dump($ref);
?>