<?php

class Foo {
    const X = __METHOD__;
}
function foo() {
    class Bar {
        const X = __METHOD__;
    }
}

foo();
var_dump(Foo::X);
var_dump(Bar::X);

?>