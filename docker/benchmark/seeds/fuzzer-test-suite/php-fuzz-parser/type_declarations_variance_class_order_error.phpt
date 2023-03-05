<?php

class A {
    public function method() : B {}
}
class B extends A {
    public function method() : C {}
}
class C extends B {
}

new C;

?>