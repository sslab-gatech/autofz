<?php
class A {
    private   static $a = "a";
    protected static $b = "b";
    public    static $c = "c";
    public function __construct() {
    var_dump($this->a, $this->b, $this->c);
    }
}
class B extends A {
}
new B;
?>