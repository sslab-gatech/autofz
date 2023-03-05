<?php
class A {
    public $foo = 1;
    public int $bar = 2;
}
class B {
    public A $a;
}
$f = function (&$n) {
    var_dump($n);
    $n = "ops";
};
$o = new B;
$o->a = new A;
$f($o->a->foo);
$f($o->a->bar);
?>