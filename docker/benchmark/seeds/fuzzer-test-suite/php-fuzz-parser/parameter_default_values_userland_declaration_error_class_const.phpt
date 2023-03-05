<?php

use Foo\Bar;

class A
{
    public function foo(
        $param1 = \Foo\Bar::CONSTANT,
        $param2 = Foo\Bar::CONSTANT,
        $param3 = Bar::CONSTANT
    ) {
    }
}

class B extends A
{
    public function foo()
    {
    }
}