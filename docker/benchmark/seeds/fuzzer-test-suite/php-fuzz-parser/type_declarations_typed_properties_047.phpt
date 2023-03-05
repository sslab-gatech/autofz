<?php
class Foo {
    public ?int $foo = null;
}

$x = new Foo();
var_dump($x);
var_dump($x->foo);

$x->foo = 5;
var_dump($x->foo);

$x->foo = null;
var_dump($x->foo);

unset($x->foo);
try {
    var_dump($x->foo);
} catch (Throwable $e) {
    echo $e->getMessage()."\n";
}
try {
    $x->foo = "ops";
} catch (Throwable $e) {
    echo $e->getMessage()."\n";
}
?>