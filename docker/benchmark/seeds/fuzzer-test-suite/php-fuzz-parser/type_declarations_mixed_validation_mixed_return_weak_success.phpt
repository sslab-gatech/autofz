<?php

function foo($a): mixed
{
    return $a;
}

foo(null);
foo(false);
foo(1);
foo("");
foo([]);
foo(new stdClass());

?>