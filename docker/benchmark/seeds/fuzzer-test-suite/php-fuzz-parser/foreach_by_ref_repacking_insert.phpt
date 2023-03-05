
<?php
$a = [];
$a[1] = 1;
foreach ($a as $k => &$v) {
    var_dump($v);
    if ($k == 1) $a[4] = 4;
    if ($k == 4) $a[2] = 2;
}

?>