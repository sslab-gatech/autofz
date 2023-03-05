<?php
for($c = -16; $c < 0; $c++) {
        var_dump($c, intdiv(PHP_INT_MIN, 10), intdiv(PHP_INT_MIN, 10) * $c);
    echo "-----------\n";
}
for($c = 0; $c <= 16; $c++) {
        var_dump($c, intdiv(PHP_INT_MAX, 10), intdiv(PHP_INT_MAX, 10) * $c);
    echo "-----------\n";
}
?>