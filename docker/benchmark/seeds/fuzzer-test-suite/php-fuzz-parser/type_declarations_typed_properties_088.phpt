<?php

class A {
    public int $prop;
}
class B {
    public $prop;
}

function test($obj) {
    $obj->prop = "42";
    var_dump($obj);
}

test(new A);
test(new B);

?>