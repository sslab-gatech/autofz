<?php
$out = new stdClass;
$out->x = $out;
mb_parse_str("a=b", $out);
var_dump(gc_collect_cycles());
?>