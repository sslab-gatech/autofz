<?php

$obj = new stdClass;
$obj->ref =& $ref;
$obj->val = $obj->ref = 42;
var_dump($obj);

?>