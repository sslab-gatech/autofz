<?php
class Foo {
    public int $bar;

    public function __get($name) {
        return "violate";
    }
}

$foo = new Foo;

$foo->bar = "1"; # ok

unset($foo->bar); # ok

var_dump($foo->bar); # not okay, __get is nasty
?>