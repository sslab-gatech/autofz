<?php

class A {
    private $prop = "1";
}
class B extends A {
    private int $prop = 2;
}

var_dump((function () { return $this->prop; })->call(new B));

?>