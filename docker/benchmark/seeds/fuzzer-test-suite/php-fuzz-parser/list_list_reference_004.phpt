<?php
$coords = array(array(1, 2), array(3, 4));
foreach ($coords as [&$x, $y]) {
    $x++;
    $y++;
}
var_dump($coords);
?>