<?php

class A {
    protected const FOO = 1;
}

class B {}
class C extends B {
    public function method() {
        var_dump(A::FOO);
    }
}
(new C)->method();

?>