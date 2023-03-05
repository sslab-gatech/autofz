<?php

abstract class A {
    abstract function __construct(X $x);
}
class B extends A {
    function __construct(X $x) {}
}
class C extends B {
    function __construct() {}
}

?>