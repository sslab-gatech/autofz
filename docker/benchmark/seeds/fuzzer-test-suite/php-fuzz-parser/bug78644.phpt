<?php

$a = new stdClass;
unset($a->b->c->d);
unset($a->b->c['d']);
var_dump($a);

?>