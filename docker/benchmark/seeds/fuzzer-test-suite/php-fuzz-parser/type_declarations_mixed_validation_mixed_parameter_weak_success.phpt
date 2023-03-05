<?php

function foo(mixed $a)
{
}

foo(null);
foo(false);
foo(1);
foo(3.14);
foo("");
foo([]);
foo(new stdClass());

?>