<?php

$a = 1;
array_map(function($x) use (&$lastval) { $lastval = $x; }, $GLOBALS);
var_dump(gettype($lastval), $lastval); // will contain $a

?>