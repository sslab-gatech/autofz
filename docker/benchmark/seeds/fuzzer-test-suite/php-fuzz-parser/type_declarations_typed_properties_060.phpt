<?php

class A {
    public int $a = 1;
}
class B extends A {}

$o = new B;
var_dump($o->a);
$o->a = "a";

?>