<?php

class X {}
class Y extends X {}

class A {
    public function method(): Y|string {}
}
class B extends A {
    public function method(): X|string {}
}

?>