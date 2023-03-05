<?php
$a = array();
$b =& $a;
$a[0] = $a;
var_dump($a);
$a = array(array());
$b =& $a;
$a[0][0] = $a;
var_dump($a);
?>