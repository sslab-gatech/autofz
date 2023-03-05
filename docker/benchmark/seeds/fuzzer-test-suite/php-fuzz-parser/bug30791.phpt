<?php

class a
{
    public $a = 4;
    function __call($name, $args) {
        echo __METHOD__, "\n";
    }
}

$b = new a;
var_dump($b);
$c = unserialize(serialize($b));
var_dump($c);

?>