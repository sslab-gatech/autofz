<?php

class Foo {
    function testParentBuiltin(int $foo) {}
    function testBothBuiltin(int $foo) {}
    function testChildBuiltin($foo) {}
    function testNoneBuiltin($foo) {}
}

class Bar extends Foo {
    function testParentBuiltin($foo) {}
    function testBothBuiltin(int $foo) {}
    function testChildBuiltin(int $foo) {}
    function testNoneBuiltin($foo) {}
}

?>