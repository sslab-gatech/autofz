<?php

class ObjectOne
{
    public $x;

    function __construct($x)
    {
        $this->x = $x;
    }

    function __toString() {
        return "Object";
    }
}

class Overloaded
{
    public $props = array();
    public $x;

    function __construct($x)
    {
        $this->x = new ObjectOne($x);
    }

    function __get($prop)
    {
        echo __METHOD__ . "($prop)\n";
        return $this->props[$prop];
    }

    function __set($prop, $val)
    {
        echo __METHOD__ . "($prop,$val)\n";
        $this->props[$prop] = $val;
    }
}
$y = new Overloaded(2);
var_dump($y->x);
var_dump($y->x->x);
var_dump($y->x->x = 3);
var_dump($y->y = 3);
var_dump($y->y);
var_dump($y->z = new ObjectOne(4));
var_dump($y->z->x);
$t = $y->z;
var_dump($t->x = 5);
var_dump($y->z->x = 6);

?>