<?php

$obj = new class {
    public ?iterable $it = null;
};

function arr(?array &$arr) {
    $arr = [1];
}

arr($obj->it);
var_dump($obj->it);
array_shift($obj->it);
var_dump($obj->it);
parse_str("foo=bar", $obj->it);
var_dump($obj->it);
$obj->it = [];
var_dump($obj->it);

?>