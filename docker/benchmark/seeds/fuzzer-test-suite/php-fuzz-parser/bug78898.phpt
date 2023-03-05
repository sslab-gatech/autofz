<?php

class A
{
    protected function _x()
    {
        echo "a";
    }

    public function __call($methodName, array $arguments)
    {
        throw new Exception("Unknown method.");
    }
}

class B extends A
{
    public function x()
    {
        parent::_x();
        call_user_func('parent::_x');
        call_user_func(['parent', '_x']);
    }
}

$b = new B;
$b->x();

?>