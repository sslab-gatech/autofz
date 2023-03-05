<?php

trait T {
    public $x = self::X;
}
trait T2 {
    public $x = self::X;
}
class C {
    use T, T2;
    const X = 42;
}
var_dump((new C)->x);

?>