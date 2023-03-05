<?php
class X {
}
abstract class A {
    abstract function __construct(X $x);
}
class B extends A {
    function __construct(object $x) {}
}
class C extends B {
    function __construct(Y $x) {}
}
?>