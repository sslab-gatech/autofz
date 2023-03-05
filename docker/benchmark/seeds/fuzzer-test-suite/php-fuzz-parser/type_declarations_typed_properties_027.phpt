<?php

class Foo {
    public float $bar = 1.1;
}

$foo = new Foo;
$foo->bar = 10;

var_dump($foo->bar);
?>