<?php

class A {

    private $foo = 0;

    public function &__get($foo){ return $this->foo; }

}

$a = new A;
echo $a->f++;
echo $a->f++;
echo $a->f++;
?>