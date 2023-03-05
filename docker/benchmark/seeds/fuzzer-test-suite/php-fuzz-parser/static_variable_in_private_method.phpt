<?php

class A {
    private function m() {
        static $x;
    }
}
class B extends A {}

?>
===DONE===