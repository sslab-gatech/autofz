<?php
$arr = array(new stdclass);
list(&$a, &$b) = $arr;
var_dump($a, $b);
var_dump($arr);
?>