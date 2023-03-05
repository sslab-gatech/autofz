<?php
class Foo {
    public int $bar = 1;
}

$cb = function(int &$bar) {
    var_dump($bar);
};

$foo = new Foo();
$cb($foo->bar);
?>