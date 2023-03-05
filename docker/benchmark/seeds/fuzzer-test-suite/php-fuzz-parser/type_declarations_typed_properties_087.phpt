<?php

class A {
    public static ?int $a;
}

$x =& A::$a;
var_dump($x);

?>