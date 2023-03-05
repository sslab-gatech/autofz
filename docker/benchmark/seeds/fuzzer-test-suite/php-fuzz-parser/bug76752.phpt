<?php
$obj = new stdClass;
$val = 'foo';
$obj->prop = &$val;
var_dump($obj->prop ?? []);
?>