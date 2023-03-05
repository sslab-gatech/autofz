<?php
class Foo {
    public int $bar = 1;
}

$foo = new Foo();
foreach ($foo as &$prop) {
    $prop++;
}
var_dump($foo);
?>