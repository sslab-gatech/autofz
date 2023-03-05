<?php

class foo {
    public function __get($a) {
        return new $this;
    }
}

$c = new foo;

$a = clone $c->b[1];

?>