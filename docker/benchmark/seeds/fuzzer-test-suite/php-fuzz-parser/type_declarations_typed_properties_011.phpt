<?php
class Foo {
    public int $bar = 1;
}

$foo = new Foo();

$array = [&$foo->bar];
var_dump($array);
?>