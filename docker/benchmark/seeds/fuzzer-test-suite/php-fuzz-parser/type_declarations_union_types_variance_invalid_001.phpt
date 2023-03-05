<?php

class A {
    public function method(): int {}
}
class B extends A {
    public function method(): int|float {}
}

?>