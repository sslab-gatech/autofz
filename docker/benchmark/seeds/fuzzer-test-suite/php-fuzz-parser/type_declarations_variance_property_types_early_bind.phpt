<?php

class X {}
class_alias('X', 'Y');

class A {
    public X $prop;
}
class B extends A {
    public Y $prop;
}

?>
===DONE===