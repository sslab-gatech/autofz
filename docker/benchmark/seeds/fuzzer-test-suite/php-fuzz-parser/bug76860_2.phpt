<?php
class A {
    private static $a = "a";
    private static $b = "b";
    private static $c = "c";
    public function __construct() {
    var_dump($this->a, $this->b, $this->c);
    }
}
class B extends A {
    private static $a = "a1";
    protected static $b = "b1";
    public static $c = "c1";
}
new B;
?>