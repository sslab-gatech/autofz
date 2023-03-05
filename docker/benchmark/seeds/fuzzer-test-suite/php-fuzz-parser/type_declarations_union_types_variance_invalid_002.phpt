<?php

class A {
    public function method(int|float $a) {}
}
class B extends A {
    public function method(int $a) {}
}

?>