<?php

class Foo {
    public ?string $a, $b;
    public ?stdClass $c, $d;
}

$t = new Foo;
$t->a = "str";
$t->b = "str";
$t->c = new stdClass;
$t->d = new stdClass;

var_dump($t->a, $t->b, $t->c, $t->d);

$t->a = null;
$t->b = null;
$t->c = null;
$t->d = null;
var_dump($t->a, $t->b, $t->c, $t->d);

?>