<?php
require __DIR__ . "/bug76451.inc";

class A {
    public function test(Foo $foo) {}
}
class B extends A {
    public function test(Bar $foo) {}
}
?>
===DONE===