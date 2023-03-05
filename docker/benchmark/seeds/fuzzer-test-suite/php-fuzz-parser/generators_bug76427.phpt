<?php
$func = function () {
    yield 2;
};

$a  = new stdclass();
$b =  new stdclass();
$a->b = $b;
$b->a = $a;

$func = $a->func = $func();

unset($b);
unset($a);
unset($func);

var_dump(gc_collect_cycles());

?>