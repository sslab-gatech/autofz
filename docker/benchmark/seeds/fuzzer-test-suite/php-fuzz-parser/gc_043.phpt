<?php
$s = <<<'STR'
O:8:"stdClass":2:{i:5;C:8:"SplStack":29:{i:4;:r:1;:O:8:"stdClass":0:{}}i:0;O:13:"RegexIterator":1:{i:5;C:8:"SplStack":29:{i:4;:r:1;:O:8:"stdClass":0:{}}}}
STR;
var_dump(unserialize($s));
gc_collect_cycles();
?>