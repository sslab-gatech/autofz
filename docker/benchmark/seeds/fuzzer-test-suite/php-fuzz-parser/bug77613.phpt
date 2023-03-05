<?php
class A {
    public function __construct() {
        static $foo;
    }
}

class B extends A { }

class C extends B {
    private function __construct() {}
}
?>
OK