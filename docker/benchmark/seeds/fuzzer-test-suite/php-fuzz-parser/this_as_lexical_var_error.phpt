<?php

class Foo {
    public function f() {
        return function() use ($this) {};
    }
}

?>