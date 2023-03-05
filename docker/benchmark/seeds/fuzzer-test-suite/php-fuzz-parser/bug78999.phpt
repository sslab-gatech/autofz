<?php
function get() {
    $t = new stdClass;
    $t->prop = $t;
    return $t;
}
var_dump(get());
var_dump(gc_collect_cycles());