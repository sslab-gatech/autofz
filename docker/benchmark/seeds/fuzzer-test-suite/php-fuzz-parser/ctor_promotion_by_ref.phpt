<?php

class Ary {
    public function __construct(public array &$array) {}
}

$array = [];
$ary = new Ary($array);
$array[] = 42;
var_dump($ary->array);

?>