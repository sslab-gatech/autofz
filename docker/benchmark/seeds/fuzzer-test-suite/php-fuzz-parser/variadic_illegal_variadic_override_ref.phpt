<?php

class A {
    public function test(&$a, &$b) {}
}

class B extends A {
    public function test(...$args) {}
}

?>