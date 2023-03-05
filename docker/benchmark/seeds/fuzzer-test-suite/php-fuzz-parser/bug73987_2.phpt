<?php

abstract class A {
    abstract function example($a, $b, $c);
}

class B extends A {
    function example($a, $b = null, $c = null) { }
}

class C extends B {
    function example($a, $b, $c = null) { }
}

?>