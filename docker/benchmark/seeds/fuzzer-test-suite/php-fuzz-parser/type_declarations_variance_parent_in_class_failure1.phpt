<?php

// Illegal: A::parent is ill-defined
class A {
    public function method(parent $x) {}
}
class B extends A {
    public function method(parent $x) {}
}

?>