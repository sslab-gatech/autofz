<?php

class Test {
    public function __destruct() {
        $GLOBALS['x'] = $this;
    }
}

$t = new Test;
$t->x = new stdClass;
$t->x->t = $t;
$a = (array) $t->x;
unset($t, $a);
gc_collect_cycles();
var_dump($x);

?>