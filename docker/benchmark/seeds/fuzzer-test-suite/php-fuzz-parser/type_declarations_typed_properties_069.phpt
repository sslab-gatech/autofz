<?php

function &nonNumericStringRef() {
    static $a = "x";
    return $a;
}

class Foo {
    public static int $i;
}

try {
    Foo::$i = &nonNumericStringRef();
} catch (TypeError $e) { print $e->getMessage()."\n"; }
try {
    var_dump(Foo::$i);
} catch (Error $e) { print $e->getMessage()."\n"; }
var_dump(nonNumericStringRef());

?>