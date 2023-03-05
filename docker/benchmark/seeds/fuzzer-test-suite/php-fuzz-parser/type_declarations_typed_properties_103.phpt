<?php
class C {
    public $a = 0;
}
function foo() {
    $x = new C;
    $x->a = 1;
    unset($x->a);
    $x->a += 2;
    var_dump($x);
}
foo();
?>