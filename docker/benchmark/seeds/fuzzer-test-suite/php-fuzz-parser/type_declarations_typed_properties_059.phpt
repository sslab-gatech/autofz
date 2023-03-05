<?php
trait T {
    public int $a1;
    public ?int $b1;
}

class A {
    use T;
    public int $a2;
    public ?int $b2;
}

$x = new A;
var_dump($x);
?>