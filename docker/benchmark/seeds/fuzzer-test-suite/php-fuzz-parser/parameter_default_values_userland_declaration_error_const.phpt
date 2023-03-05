<?php

use const Foo\CONSTANT;

class A
{
    public function foo(
        $param1 = \Foo\CONSTANT,
        $param2 = Foo\CONSTANT,
        $param3 = CONSTANT
    ) {
    }
}

class B extends A
{
    public function foo()
    {
    }
}