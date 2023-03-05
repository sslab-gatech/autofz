<?php

$it = new ArrayIterator([1, 2, 3]);
$it = new IteratorIterator($it);
foreach ($it as $v) {
    if (method_exists($it, 'offsetGet')) {
        var_dump($it->offsetGet(0));
    }
}

?>