<?php

class A {
    public function test(int $a, int $b) {}
}

class B extends A {
    public function test(string ...$args) {}
}

?>