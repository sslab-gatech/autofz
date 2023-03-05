<?php

function gen($iter, &$gen) {
    foreach ($iter as $v) {
        yield;
    }
}

$iter = new ArrayIterator([1, 2, 3]);
$gen = gen($iter, $gen);
$gen->next();
unset($gen);
gc_collect_cycles();

?>
===DONE===