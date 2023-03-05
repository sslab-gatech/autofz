<?php

class A {
        public int $foo;
}

class B {
        public A $foo;
}

$objs = [new A, new A];
$v = 1;

foreach ($objs as $obj) {
        $obj->foo = $v;
        $v = new A;
        $obj = new B;
        $obj->foo = $v;
}

var_dump($objs);

?>