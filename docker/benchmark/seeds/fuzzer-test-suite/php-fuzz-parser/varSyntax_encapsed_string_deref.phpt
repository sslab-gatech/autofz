<?php

$bar = "bar";
var_dump("foo$bar"[0]);
var_dump("foo$bar"->prop);
try {
    var_dump("foo$bar"->method());
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

class FooBar { public static $prop = 42; }
var_dump("foo$bar"::$prop);

function foobar() { return 42; }
var_dump("foo$bar"());

?>