<?php

class Foo {
    public int $bar = 1;
}

$foo = new Foo;
$foo->bar = "10";

var_dump($foo->bar);
?>