<?php
$a = array();
$a[] =& $a;
unset($a);
var_dump(gc_status());
gc_collect_cycles();
gc_collect_cycles();
var_dump(gc_status());