<?php

class A {
    public function test() {
        static $x;
    }
}
class B extends A {}

?>
===DONE===