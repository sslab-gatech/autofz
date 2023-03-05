<?php
$z = unserialize('O:1:"A":0:{}');
@var_dump($z->e.=0);
@var_dump(++$z->x);
@var_dump($z->y++);

$y = array(PHP_INT_MAX => 0);
try {
    var_dump($y[] .= 0);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump(++$y[]);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
try {
    var_dump($y[]++);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>