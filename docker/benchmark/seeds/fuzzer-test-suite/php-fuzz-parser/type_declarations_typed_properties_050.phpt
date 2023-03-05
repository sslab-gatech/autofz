<?php

$b = 1;
$a = "$b";
class A { public int $a; }
$o = new A;
$o->a = $b;
var_dump($o, $a);

?>