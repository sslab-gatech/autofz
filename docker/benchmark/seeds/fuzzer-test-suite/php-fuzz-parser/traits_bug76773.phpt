<?php

trait MyTrait
{
    public function hello()
    {
        echo __CLASS__, "\n";

        if (\is_callable(array('parent', __FUNCTION__))) {
            parent::hello();
        }
    }
}

class ParentClass
{
    use MyTrait;
}

class ChildClass extends ParentClass
{
    use MyTrait;
}

$c = new ChildClass();
$c->hello();