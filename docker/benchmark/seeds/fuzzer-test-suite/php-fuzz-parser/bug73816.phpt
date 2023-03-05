<?php

function anon()
{
    static $i = 0;
    return eval(sprintf('return new class { private $prop%s; };', ++$i));
}

var_dump(anon());
var_dump(anon());

?>