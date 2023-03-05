<?php

function test1(integer $x) {}
function test2(double $x) {}
function test3(boolean $x) {}
function test4(resource $x) {}

namespace Foo {
    use integer as foo;

    function test5(\integer $x) {}
    function test6(namespace\integer $x) {}
    function test7(foo $x) {}
    function test8(boolean $x) {}
}

namespace Foo {
    use integer;
    function test9(integer $x) {}
}

namespace {
    use integer as foo;

    function test10(\integer $x) {}
    function test11(namespace\integer $x) {}
    function test12(foo $x) {}
    function test13(boolean $x) {}
}

?>