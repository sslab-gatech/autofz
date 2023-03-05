<?php

class Arr
{
    private $foo = '';

    public function __construct(array $array = [])
    {
        $property = 'foo';

        $this->{$property} = &$array[$property];

        \var_dump($this->foo);
    }
}

$arr = new Arr(['foo' => 'bar']);
?>