<?php
declare(strict_types=1);

class Foo {
    public int $bar;

    public function __get($name) {
        var_dump($name);
    }
}

$foo = new Foo();

unset($foo->bar);
var_dump($foo->bar);
?>