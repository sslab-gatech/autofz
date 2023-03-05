<?php
$arr = array(1, array(2));
list(&$a, list(&$b)) = $arr;
var_dump($a, $b);
var_dump($arr);

$arr = array(1, array(2));
list($a, &$b) = $arr;
var_dump($arr);

$arr = array(1, array(2));
[&$a, [&$b]] = $arr;
var_dump($a, $b);
var_dump($arr);

$arr = array(1, array(2));
[&$a, [&$b], &$c] = $arr;
var_dump($a, $b, $c);
var_dump($arr);

$arr = array("one" => 1, "two" => array(2));
["one" => &$a, "two" => [&$b], "three" => &$c] = $arr;
var_dump($a, $b, $c);
var_dump($arr);
?>