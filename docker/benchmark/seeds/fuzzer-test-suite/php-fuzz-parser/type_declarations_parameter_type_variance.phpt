<?php

class Foo {
    function testParentClass(Foo $foo) {}
    function testBothClass(Foo $foo) {}
    function testChildClass($foo) {}
    function testNoneClass($foo) {}
}

class Bar extends Foo {
    function testParentClass($foo) {}
    function testBothClass(Foo $foo) {}
    function testChildClass(Foo $foo) {}
    function testNoneClass($foo) {}
}

?>