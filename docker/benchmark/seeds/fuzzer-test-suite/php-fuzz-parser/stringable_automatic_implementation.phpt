<?php

class Test {
    public function __toString() {
        return "foo";
    }
}

var_dump(new Test instanceof Stringable);
var_dump((new ReflectionClass(Test::class))->getInterfaceNames());

class Test2 extends Test {
    public function __toString() {
        return "bar";
    }
}

var_dump(new Test2 instanceof Stringable);
var_dump((new ReflectionClass(Test2::class))->getInterfaceNames());

?>