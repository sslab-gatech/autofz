<?php
$ary = [[0, 1]];
[[
    0 => &$a,
    ($ary["foo"] = 1) => &$b
]] = $ary;

var_dump($ary, $a, $b);
unset($ary, $a, $b);

$ary = [[0, 1]];
[
    0 => &$a,
    ($ary["foo"] = 1) => &$b
] = $ary[0];
var_dump($ary, $a, $b);
?>