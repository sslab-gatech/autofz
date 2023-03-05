<?php

class Test {
    public $prop = 'default value';
}

$obj = new Test;
$obj->{1} = null;

$arr = (array) $obj;
$arr['prop'] = 'new value';

echo $obj->prop, "\n";

?>