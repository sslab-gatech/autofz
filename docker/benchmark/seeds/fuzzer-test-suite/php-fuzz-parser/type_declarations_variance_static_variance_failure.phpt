<?php

class A {
    public function test(): static {}
}
class B extends A {
    public function test(): self {}
}

?>