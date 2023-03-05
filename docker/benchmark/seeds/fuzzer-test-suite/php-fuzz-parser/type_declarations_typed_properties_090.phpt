<?php

class A {
    private int $prop = 42;

    public function test() {
        $x =& $this->prop;
        unset($this->prop);
        $x = "foo";
        var_dump($x);
    }
}
class B extends A {
    private $prop;
}

$b = new B;
$b->test();

?>