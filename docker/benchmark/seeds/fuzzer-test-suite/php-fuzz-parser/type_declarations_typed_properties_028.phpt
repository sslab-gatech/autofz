<?php
class Foo {
    public int $bar;
}

$foo = new Foo;
$foo->bar = "1";

var_dump($foo->bar);
?>