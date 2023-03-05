<?php

abstract class A {
    abstract function example();
}

class B extends A {
    function example(): int  { }
}

class C extends B {
    function example(): string { }
}

?>